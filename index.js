const express = require('express');
const app = express();
const getMenu = require('./get-menu');
const getRestaurants = require('./get-restaurants');
const fs = require('fs');
const _ = require('lodash');
const bodyParser = require('body-parser');
const exec = require('child_process').exec;
const morgan = require('morgan');
app.use((req, res, next) => {
  console.log('REQUEST', req.url);
  next();
});
//app.use(morgan('combined'));
app.use(bodyParser());

app.get('/menus', (req, res) => {
  const address = req.query.address;
  const numFoods = req.query.foods;
  console.log(req.body, address, numFoods);
  fs.readFile('types.json', 'utf8', function(err, data) {
    if (err) {
      console.log(err);
      res.status(err.status || 400);
      res.json({ err });
    }

    let json = JSON.parse(data);

    getRestaurants(address).then(response => {
      console.log(response.data);
      let restaurants = response.data.restaurants.map(r => {
        return {
          apiKey: r.apiKey,
          foodTypes: r.foodTypes.map(foodType => {
            let newType = _.filter(_.keys(json), key => {
              return _.includes(json[key], foodType);
            })[0];

            if (_.isEmpty(newType)) {
              return 'Other';
            }

            return newType.replace(/ /g, '-');
          }),
          maxWaitTime: r.maxWaitTime,
          minWaitTime: r.minWaitTime,
          deliveryMin: r.deliveryMin,
          name: r.name
            .replace(/\'/g, '')
            .replace(/\"/g, '')
            .replace(/\n/g, ''),
          streetAddress: r.streetAddress,
          open: r.open,
          latitude: r.latitude,
          longitude: r.longitude
        };
      });
      //let userPreferences = req.user.preferences.map(preference => preference.category);
      const userPreferences = Object.keys(req.query).map(key => key != 'address' && key != 'foods');

      console.log('PREFERENCES: ', userPreferences);
      let restaurantString = `'${JSON.stringify({
        address: response.data.address,
        restaurants: restaurants,
        preferences: userPreferences,
        price: 5,
        foods: numFoods //numfoods??
      })}'`;

      exec(`python3 selection/restaurantSelection.py ${restaurantString}`, function(
        error,
        stdout,
        stderr
      ) {
        if (error !== null) {
          console.log('exec error: ' + error);
        }

        let restaurantKey = stdout.replace('\n', '');
        getMenu(restaurantKey).then(menuResponse => {
          console.log('MENURESPONSE', menuResponse.data);
          let menuItems = _.flatten(
            menuResponse.data.map(menu => {
              return menu.items.map(item => {
                return {
                  apiKey: item.apiKey,
                  basePrice: item.basePrice,
                  name: item.name
                    .replace(/\n/g, '')
                    .replace(/\(/g, '')
                    .replace(/\)/g, '')
                    .replace(/"/g, '')
                    .replace(/'/g, '')
                };
              });
            })
          );

          let menuString = `'${JSON.stringify({ menu: menuItems, price: 20 })}'`;
          let mkeys = [];
          let co = 0;
          for (let i = 0; i < numFoods; ++i) {
            exec(`python3 selection/menuSelection.py ${menuString}`, function(
              // TODO: USER SETS PRICE
              error,
              stdout,
              stderr
            ) {
              ++co;
              if (error !== null) {
                console.log('exec error: ' + error);
              }

              let menuItemKeys = JSON.parse(
                `{ "items": ${stdout.replace('\n', '').replace(/'/g, '"')}}`
              ).items;

              menuItemKeys.forEach(key => {
                mkeys.push(key);
                console.log(mkeys);
              });
              if (co == numFoods) {
                res.json({ restaurantKey: restaurantKey, menuItems: mkeys });
              }
            });
          }
          console.log('MKEYS: ', Object.keys(mkeys));
        });
      });
    });
  });
});

app.get('/categories', function(req, res) {
  fs.readFile('types.json', 'utf8', function(err, data) {
    if (err) {
      console.log(err);
      res.status(err.status || 400);
      res.json({ err });
    }

    let json = JSON.parse(data);

    res.json({
      categories: _.keys(json).map(key => {
        return key.replace(' ', '-');
      })
    });
  });
});

app.listen(process.env.PORT || 3000);

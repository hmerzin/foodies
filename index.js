const express = require('express');
const app = express();
const getMenu = require('./get-menu');
const getRestaurants = require('./get-restaurants');
const fs = require('fs');
const _ = require('lodash');
const bodyParser = require('body-parser');
const exec = require('child_process').exec;
app.use(bodyParser());

app.get('/menus', (req, res) => {
  const address = req.query.address;
  const numFoods = req.query.foods;
  fs.readFile('types.json', 'utf8', function(err, data) {
    if (err) {
      console.log(err);
      res.status(err.status || 400);
      res.json({ err });
    }

    let json = JSON.parse(data);

    getRestaurants(address).then(response => {
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
      const userPreferences = req.body.preferences
        .filter(prefObj => {
          return prefObj[Object.keys(prefObj)[0]] == 1;
        })
        .map(prefObj => {
          return Object.keys(prefObj)[0];
        });
      console.log('PREFERENCES: ', userPreferences);
      let restaurantString = `'${JSON.stringify({
        address: response.data.address,
        restaurants: restaurants,
        preferences: userPreferences,
        price: 20,
        foods: numFoods //numfoods??
      })}'`;

      let restaurantKey = "";
      let menuItems = [];

      exec(`python3 selection/restaurantSelection.py ${restaurantString}`, function(
        error,
        stdout,
        stderr
      ) {
            if (error !== null) {
              console.log('exec error: ' + error);
              res.json({ restaurantKey: "", menuItems: [] });
            } else {
              restaurantKey = stdout.replace('\n', '');
              if (restaurantKey.includes("ERROROHCRAP")) {
                console.log("THERE WAS AN ERROR, NO RESTAURANT", stdout);
                res.json({ restaurantKey: "", menuItems: [] });
              } else {
                getMenu(restaurantKey).then(menuResponse => {
                  menuItems = _.flatten(
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
                });
              }
            }  
          let menuString = `'${JSON.stringify({ menu: menuItems, price: 20 })}'`;
          let mkeys = [];
          let co = 0;
          for (let i = 0; i < numFoods; ++i) {
            exec(`python3 selection/menuSelection.py ${menuString}`, function(
              error,
              stdout,
              stderr
            ) {
              ++co;
              let menuItemKeys = [];
              if (error !== null || (stdout.replace('\n','')).includes("ERROROHCRAP")) {
                console.log('exec error: ' + error);
              } else {
                menuItemKeys = JSON.parse(
                  `{ "items": ${stdout.replace('\n', '').replace(/'/g, '"')}}`
                ).items;
                menuItemKeys.forEach(key => {
                  mkeys.push(key);
                  console.log(mkeys);
                });
              }
              if (co == numFoods) {
                res.json({ restaurantKey: restaurantKey, menuItems: mkeys });
              }
            });
          }
          console.log('MKEYS: ', Object.keys(mkeys));
          res.json({ restaurantKey: restaurantKey, menuItems: mkeys });
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

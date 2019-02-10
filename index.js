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
        if (error !== null || stderr.includes('OHCRAP') || stdout.includes('OHCRAP')) {
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

const types = {
  Juices: ['Smoothies & Juices', 'Juice Bars & Smoothies', 'Juices'],
  Irish: ['Irish', 'Bar/Pub Food', 'Pubs', 'Bars', 'Irish Pub', 'Bar Food'],
  Italian: ['Pasta', 'Italian Food', 'Italian', 'Pizza', 'Calabrian', 'Panini'],
  American: [
    'Chicken Wings',
    'American (New)',
    'Southern Food',
    'Barbeque',
    'Sports Bars',
    'American Food',
    'American',
    'American (Traditional)',
    'Hot Dogs',
    'BBQ',
    'Southern',
    'Hot Dog',
    'Tex-Mex',
    'Burgers',
    'Steakhouses',
    'Wings',
    'Comfort Food',
    'Chicken'
  ],
  French: ['French Food', 'French', 'Belgian', 'Bistro'],
  Sandwiches: [
    'Sandwiches',
    'Sandwich',
    'Delis',
    'Meat Shops',
    'Deli',
    'Subs & Sandwiches',
    'Chicken Shop'
  ],
  Dessert: ['Dessert', 'Ice Cream', 'Ice Cream & Frozen Yogurt', 'Desserts', 'Bakery', 'Bakeries'],
  Asian: [
    'Dim Sum',
    'Szechuan',
    'Thai',
    'Asian Food',
    'Chinese',
    'Asian Fusion',
    'Fusion',
    'Vietnamese Food',
    'Korean',
    'Thai Food',
    'Malaysian',
    'Chinese Food',
    'Taiwanese',
    'Laotian',
    'Vietnamese',
    'Korean Food',
    'Asian',
    'Noodles'
  ],
  'Middle Eastern': [
    'Moroccan',
    'Halal',
    'Falafel',
    'Turkish',
    'Middle Eastern',
    'Pakistani',
    'Pakistani Food',
    'Middle Eastern Food',
    'Lebanese',
    'Turkish Food',
    'Armenian'
  ],
  Mexican: [
    'Latin American',
    'Brazilian',
    'Tacos',
    'Mexican Food',
    'Latin American Food',
    'Mexican',
    'Caribbean Food'
  ],
  Indian: [
    'indian',
    'Indian Food',
    'Himalayan & Nepalese Food',
    'Himalayan/Nepalese',
    'Indian',
    'Bangladeshi'
  ],
  Greek: ['Mediteranean', 'Greek', 'Greek Food', 'Mediterranean Food', 'Buffets', 'Mediterranean'],
  Seafood: ['Seafood Markets', 'Seafood'],
  Japanese: ['Sushi Bars', 'Japanese Food', 'Sushi', 'Japanese', 'Ramen'],
  Breakfast: [
    'Breakfast',
    'Breakfast & Brunch',
    'Coffee',
    'Coffee & Tea',
    'Cafes',
    'Cafe',
    'Bagels',
    'Brunch'
  ],
  Alcohol: ['Wine Bars', 'Cocktail Bars', 'Beer'],
  Other: [
    'Convience',
    'Caterers',
    'Grocery',
    'Convenience Store',
    'Food Delivery Services',
    'Food Trucks',
    'Gluten Free',
    'Vegan',
    'Vegetarian',
    'Catering',
    'Venues & Event Spaces',
    'Groceries',
    'Convenience Stores',
    'Market',
    'Gluten-Free',
    'Food',
    'Healthy',
    'Soup',
    'Fast Food',
    'Healthy Food',
    'Salads',
    'Salad',
    'Cheese Shops',
    ''
  ]
};

app.get('/categories', function(req, res) {
  res.json({
    categories: _.keys(types).map(key => {
      return key.replace(' ', '-');
    })
  });
});

app.listen(process.env.PORT || 3000);

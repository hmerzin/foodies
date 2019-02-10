const axios = require('axios');
const apikey = require('./apikey');
const getRestaurants = address => {
  /**
   * Address must be:
   * HouseNumber, Street, City, State
   */
  const requestConfig = {
    headers: { 'X-Access-Token': apikey, 'Content-Type': 'application/json' }
  };
  const uri = `https://api.eatstreet.com/publicapi/v1/restaurant/search?method=delivery&street-address=${address
    .split(' ')
    .join('+')}`;
  return axios.get(uri, requestConfig);
};
module.exports = getRestaurants;

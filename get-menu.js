const axios = require('axios');
const apikey = require('./apikey');
const getMenu = restaurant => {
  /**
   * Address must be:
   * HouseNumber, Street, City, State
   */
  const requestConfig = { headers: { 'X-Access-Token': apikey } };
  const uri = `https://api.eatstreet.com/publicapi/v1/restaurant/${restaurant}/menu?includeCustomizations=false`;
  return axios.get(uri, requestConfig);
};

module.exports = getMenu;

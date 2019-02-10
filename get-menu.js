const axios = require('axios');
const apikey = require('./apikey');
const getMenu = restaurant => {
  console.log("ENTERING GETMENU");
  /**
   * Address must be:
   * HouseNumber, Street, City, State
   */
  const requestConfig = { headers: { 'X-Access-Token': apikey } };
  const uri = `https://api.eatstreet.com/publicapi/v1/restaurant/${restaurant}/menu?includeCustomizations=false`;

  console.log(requestConfig);
  console.log(restaurant);
  console.log(axios.get(uri, requestConfig));
  console.log("EXITING GETMENU");

  return axios.get(uri, requestConfig);
};

module.exports = getMenu;


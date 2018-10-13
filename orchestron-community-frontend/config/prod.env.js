'use strict'
const conf = require('../configure.json')

module.exports = {
  NODE_ENV: '"production"',
  API_URL: JSON.stringify(conf.API_URL)
};

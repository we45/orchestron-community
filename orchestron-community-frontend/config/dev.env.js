'use strict'
const merge = require('webpack-merge')
const prodEnv = require('./prod.env')
const conf = require('../configure.json')


module.exports = merge(prodEnv, {
  NODE_ENV: '"development"',
  API_URL: JSON.stringify(conf.API_URL)
})

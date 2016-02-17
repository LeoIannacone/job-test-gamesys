global.Promise = Promise
global.sinon = require('sinon')
global.jsdom = require('jsdom').jsdom(
  '<!doctype html><html><body><main id="main"></main></body></html>',
  {
    url: 'http://localhost'
  }
)
global.document = global.jsdom
global.document.documentElement.clientHeight = 500
global.window = global.document.defaultView
global.navigator = global.window.navigator
global.location = global.window.location
global.HTMLElement = function () {}

global.chai = require('chai')
global.chai.use(require('sinon-chai'))
global.expect = global.chai.expect
global._ = require('lodash')
const React = global.React = require('react')
const TestUtils = global.TestUtils = require('react-addons-test-utils')
const ReactDOM = global.ReactDOM = require('react-dom')
global.$R = require('rquery')(global._, React, ReactDOM, TestUtils)
global.chai = require('chai')
global.chai.use(function (chai, utils) {
  require('chai-react')(chai, utils, React, TestUtils)
})

global.defer = require('./test-helpers/defer')

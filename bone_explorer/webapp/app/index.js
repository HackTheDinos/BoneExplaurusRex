var _ = require('underscore/underscore.js');
var Backbone = require('backbone/backbone.js');
var search = require('./search/main.js');
var details = require('./details/main.js');

require('normalize-css/normalize.css');
require('./index.scss');

var Router = Backbone.Router.extend({
  routes: {
    ''           : 'index',
    '/'          : 'index',
    'scans/:id' : 'details'
  },

  index: function () {
    search();
  },

  details: function (id) {
    details(id);
    window.location.reload();
  }
});

new Router();
Backbone.history.start();

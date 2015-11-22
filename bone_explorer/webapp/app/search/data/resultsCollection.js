var _ = require('underscore/underscore.js');
var Backbone = require('backbone/backbone.js');

var Collection = Backbone.Collection.extend({
  parse: function (response) {
    return _.pluck(response, '_source');
  }
});

module.exports = new Collection();

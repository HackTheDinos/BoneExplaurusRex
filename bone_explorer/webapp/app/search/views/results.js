var _ = require('underscore/underscore.js');
var Backbone = require('backbone/backbone.js');
var results = require('../data/resultsCollection.js');

module.exports = function () {
  var View = Backbone.View.extend({
    el: '.search--results',

    initialize: function (options) {
      this.collection = results;
      this.collection.on('reset', this.render, this);
    },

    render: function () {
      this.$el.empty();
      this.collection.toJSON().forEach(function (model) {
        var item = document.createElement('div');
        item.classList.add('search--results-item');
        var heading = document.createElement('h2');
        var headingText = document.createTextNode(model.genus + ' ' + model.species);
        heading.appendChild(headingText);
        this.el.appendChild(item);
      }, this);
    }
  });

  return new View();
};

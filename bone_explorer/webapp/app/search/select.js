var $ = require('jquery/dist/jquery.js');
var selectize = require('selectize/dist/js/standalone/selectize.js');
var elasticsearch = require('elasticsearch/src/elasticsearch.js');

require('selectize/dist/css/selectize.default.css');

module.exports = function (main, type) {
  var selectElement = document.createElement('select');
  selectElement.classList.add('search--' + type + '-select');
  main.appendChild(selectElement);

  $(selectElement).selectize({
    valueField: 'text',
    labelField: 'text',
    searchField: 'text',
    create: false,
    plugins: ['remove_button'],
    load: function(query, callback) {
        if (!query.length) return callback();

        var client = new elasticsearch.Client({
          host: 'https://wtfk1moh2k:hwf9jytoe8@boneexplorus-7582625496.us-east-1.bonsai.io',
          log: 'trace'
        });

        client.suggest({
          body: {
            suggest: {
              text: query,
              completion: {
                field: type + '_suggest'
              }
            }
          }
        }).then(function (res) {
          callback(res.suggest[0].options);
        }, callback);
    }
  });

  return selectElement.selectize;
};

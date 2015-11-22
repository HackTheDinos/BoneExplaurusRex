var elasticsearch = require('elasticsearch/src/elasticsearch.js');

function renderPreview(result) {

}

function renderContent(result) {

}

function renderHeading(result) {
  var heading = document.createElement('h2');
  heading.appendChild(document.createTextNode(result.genus + ' ' + result.species));
  document.appendChild(heading);
}

module.exports = function (id) {
    var main = document.querySelector('.main');
    main.innerHTML = '';

    var client = new elasticsearch.Client({
      host: 'https://wtfk1moh2k:hwf9jytoe8@boneexplorus-7582625496.us-east-1.bonsai.io',
      log: 'trace'
    });

    client.get({
      index: 'ct_scans',
      type: 'scan',
      id: id,
      fields: [
        'genus',
        'species'
      ]
    }).then(function (response) {
      var result = {
        genus: response.fields.genus[0],
        species: response.fields.genus[0],
        id: response['_id']
      };

      renderPreview(result);
      renderHeading(result);
      renderContent(result);
    });
};

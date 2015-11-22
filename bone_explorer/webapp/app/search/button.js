var elasticsearch = require('elasticsearch/src/elasticsearch.js');
var _ = require('underscore/underscore.js');

var selectMenus;

function submitSearch() {
  var client = new elasticsearch.Client({
    host: 'https://wtfk1moh2k:hwf9jytoe8@boneexplorus-7582625496.us-east-1.bonsai.io',
    log: 'trace'
  });

  var terms = selectMenus.map(function (menu) {
    var value = menu.getValue();
    if (value === '') {
      return;
    }
    if (menu.$dropdown[0].classList.contains('search--genus-select')) {
      return { term: { genus: value } };
    } else {
      return { term: { species: value } };
    }
  });

  terms = terms.filter(function (term) {
    return typeof term !== 'undefined';
  });

  var search;
  if (!terms.length) {
    search = client.search();
  } else {
    search = client.search({
      body: {
        query: {
          filtered: {
            filter: {
              bool: {
                must: terms
              }
            }
          }
        }
      }
    });
  }

  search.then(function (response) {
    var mainContainer = document.querySelector('.main');
    mainContainer.classList.add('-loaded');

    var resultsContainer = document.querySelector('.search--results');
    resultsContainer.innerHTML = '';

    var results = response.hits.hits.map(function (result) {
      var obj = result['_source'];
      obj.id = result['_id'];
      return obj;
    });

    var hasAnyUri = _.some(results, function (result) { return result.s3uri; });

    if (hasAnyUri) {
      var selectAllCheckbox = document.createElement('input');
      selectAllCheckbox.setAttribute('type', 'checkbox');
      selectAllCheckbox.setAttribute('name', 'download');
      selectAllCheckbox.setAttribute('value', 'all');
      selectAllCheckbox.appendChild(document.createTextNode('Download All'));
      resultsContainer.appendChild(selectAllCheckbox);

      var downloadButton = document.createElement('button');
      downloadButton.classList.add('button', 'search--results-download');
      downloadButton.appendChild(document.createTextNode('Download'));
      resultsContainer.appendChild(downloadButton);
    }

    results.forEach(function (model) {
      var item = document.createElement('div');
      item.classList.add('search--results-item');

      if (model.s3uri) {
        var checkbox = document.createElement('input');
        checkbox.setAttribute('type', 'checkbox');
        checkbox.setAttribute('name', 'download[]');
        checkbox.setAttribute('value', model.s3uri);
        item.appendChild(checkbox);
      }

      if (model.thumbnail) {
        var thumbnail = document.createElement('img');
        thumbnail.setAttribute('src', model.thumbnail);
        item.appendChild(thumbnail);
      }

      if (model.id) {
        var headingLink = document.createElement('a');
        headingLink.setAttribute('href', '#scans/' + model.id);
      }

      var heading = document.createElement('h2');
      var headingText = document.createTextNode(model.genus + ' ' + model.species);
      heading.appendChild(headingText);

      if (model.id) {
        headingLink.appendChild(heading);
        item.appendChild(headingLink);
      } else {
        item.appendChild(heading);
      }

      resultsContainer.appendChild(item);
    });


  }, function () {

  });
}

module.exports = function (main, menus) {
  var searchButton = document.createElement('button');
  var searchButtonText = document.createTextNode('Search');
  searchButton.classList.add('search--button', 'button');
  searchButton.appendChild(searchButtonText);
  main.appendChild(searchButton);

  selectMenus = menus;

  searchButton.addEventListener('click', submitSearch, false);
}

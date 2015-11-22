var selectModule = require('./select.js');
var buttonModule = require('./button.js');
require('./main.scss');

module.exports = function () {
    var main = document.querySelector('.main');
    main.innerHTML = '';
    var genusSelect = selectModule(main, 'genus');
    var speciesSelect = selectModule(main, 'species');
    var results = document.createElement('section');
    results.classList.add('search--results');
    buttonModule(main, [genusSelect, speciesSelect]);
    main.appendChild(results);
};

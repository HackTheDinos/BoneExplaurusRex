var elasticsearch = require('elasticsearch/src/elasticsearch.js');
// var Three = require('three/three.js');
// var ObjSTL = require('./objstl.js');
// var viewer = require('./stl_viewer.js');
require('./main.scss');

var main = document.querySelector('.main');

function renderPreview(result) {
  loadStl(result.stl_uri);
  // var webgl = document.createElement('div');
  // webgl.setAttribute('id', 'webgl');
  // main.appendChild(webgl);
  // viewer('https://s3.amazonaws.com/ctscans/Alioramus.stl');
  // var image = document.createElement('img');
  // image.setAttribute('src', 'https://placekitten.com/1140/400');
  // main.appendChild(image);
}

function renderContent(result) {
  var content = document.createElement('p');
  content.classList.add('detail-content');
  content.appendChild(document.createTextNode(result.content));
  main.appendChild(content);
}

function renderHeading(result) {
  var heading = document.createElement('h2');
  heading.appendChild(document.createTextNode(result.genus + ' ' + result.species));
  main.appendChild(heading);

  var date = document.createElement('h3');
  date.appendChild(document.createTextNode(result.date));
  main.appendChild(date);

  var scientist = document.createElement('h3');
  scientist.appendChild(document.createTextNode(result.scientist));
  main.appendChild(scientist);

  var institution = document.createElement('h3');
  institution.appendChild(document.createTextNode(result.institution));
  main.appendChild(institution);
}

module.exports = function (id) {
    main.innerHTML = '';

    var client = new elasticsearch.Client({
      host: 'https://wtfk1moh2k:hwf9jytoe8@boneexplorus-7582625496.us-east-1.bonsai.io',
      log: 'trace'
    });

    client.get({
      index: 'ct_scans',
      type: 'scan',
      id: id
    }).then(function (response) {
      var result = response['_source'];

      renderPreview(result);
      renderHeading(result);
      renderContent(result);
    }, function () {
      console.log('There was an error loading the scan.');
    });

    // var result = {
    //   genus: 'foo',
    //   species: 'bar',
    //   date: '11/11/11',
    //   scientist: 'scientist',
    //   institution: 'institution',
    //   content: 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Suspendisse volutpat tempus elit in ullamcorper. Aliquam dictum mauris lacus, vel venenatis nibh tempus ut. Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Cras cursus purus ante, sit amet ornare ipsum egestas id. Class aptent taciti sociosqu ad litora torquent per conubia nostra, per inceptos himenaeos. Nam laoreet eu tortor nec vulputate. Nunc vel dolor at felis iaculis condimentum non ut est. Integer ornare eget lectus eu consectetur. Vivamus vehicula consectetur justo, nec accumsan libero auctor eu. Proin lacinia sodales lacus, non volutpat diam lacinia eget. Vestibulum rhoncus elit in justo tincidunt eleifend.'
    // };
    //
    // renderPreview(result);
    // renderHeading(result);
    // renderContent(result);
};

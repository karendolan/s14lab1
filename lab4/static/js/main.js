'use strict';

let data = [];

d3.json('/load_data').then(d => {
  console.log(d.users);
  data = d.users;

  // print user count
  d3.select('#users').append('span')
    .text(data.length);

    // Instantiate
    //bars =  new Bars(data, _target='vis1');
    const bars =  new Bars(data, 'vis1');

}).catch(err => console.log(err));


var width = 960,
    height = 500,
    outerRadius = height / 2 - 1,
    innerRadius = 120;

var parseDate = d3.time.format('%Y-%m-%d %H:%M:%S').parse;

var angle = d3.time.scale()
    .range([0, 2 * Math.PI]);

var radius = d3.scale.linear()
    .range([innerRadius, outerRadius]);

var z = d3.scale.category20c();

var svg = d3.select("body").append("svg")
    .attr("width", width)
    .attr("height", height)
  .append("g")
    .attr("transform", "translate(" + width / 2 + "," + height / 2 + ")");

d3.json("/data/hour", function(error, data) {
    console.log(data);
    

});

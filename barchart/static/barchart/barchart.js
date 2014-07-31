
var windowWidth = (window.innerWidth > 0) ? window.innerWidth : screen.width;
var windowHeight = (window.innerHeight > 0) ? window.innerHeight : screen.height;

var margin = {top: 20, right: 30, bottom: 30, left: 40},
	width = windowWidth - margin.left - margin.right,
	height = windowHeight - margin.top - margin.bottom;

var xscale = d3.scale.ordinal()
  .rangeRoundBands([0, width], .1);

var yscale = d3.scale.linear()
  .range([height, 0]);

var xAxis = d3.svg.axis()
  .scale(xscale)
  .orient("bottom");

var yAxis = d3.svg.axis()
  .scale(yscale)
  .orient("left");

var chart = d3.select(".chart")
	  .attr("width", width + margin.left + margin.right)
	  .attr("height", height + margin.top + margin.bottom)
	.append("g")
	  .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

function type(d) {
  d.value = +d.value; // coerce to number
  return d;
}

var data = d3.csv.parse(d3.select("#csvdata").html(), type);

xscale.domain(data.map(function(d) { return d.name; }));
yscale.domain([0, Math.max(d3.max(data, function(d) { return d.value; }),110)]);

chart.append("g")
  .attr("class", "x axis")
  .attr("transform", "translate(0," + height + ")")
  .call(xAxis);

chart.append("g")
  .attr("class", "y axis")
  .call(yAxis);

chart.selectAll(".bar")
	.data(data)
  .enter().append("g").each( function(d) {
	var xVal = xscale(d.name);
	var yVal = yscale(d.value);
	var heightVal = height - yscale(d.value);
	var widthVal = xscale.rangeBand();
	d3.select(this).append("rect")
	  .attr("class", function(d) { return d.value > 80 ? "bar" : "bar warning"})
	  .attr("x", xVal)
	  .attr("y", yVal)
	  .attr("height", heightVal)
	  .attr("width", widthVal)
	d3.select(this).append("text")
	  .attr("class", "bartext")
	  .attr("x", xVal + widthVal / 2)
	  .attr("y", yVal)
	  .attr("dx", "-.5em")
	  .attr("dy", "1em")
	  .text(function(d) { return d.value.toString() + "%"; });
  });
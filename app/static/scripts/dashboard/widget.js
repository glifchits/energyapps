define(['knockout'], function(ko) {
    var Widget = function(title, type, measure, baseurl, params, agg2) {
        var self = this;
        self.title = title;
        self.chartId = self.title.replace(' ', '') + Math.round(Math.random() * 100);
        self.type = type;
        self.params = params;
        self.agg2 = agg2;
        self.text1 = 'text1';
        self.text2 = 'text2';
        self.value = ko.observable(0);
        self.comp = ko.observable(0);
        self.chart = ko.observable(false);
        self.fullSeries = ko.observable();

        self.computedValue = ko.computed(function() {
            if (type === "abs")
                return self.value();
            else {
                num = self.value();
                comp = self.comp();
                return (num-comp) / comp;
            }
        });

        self.displayValue = ko.computed(function() {
            num = self.computedValue().toFixed(2);
            if (type === "abs") {
                if (measure === "cost")
                    return "$" + num;
                else
                    return (num/1000).toFixed(2) + " kWh";
            }
            else {
                if (num > 0)
                    return num + "% more";
                else
                    return -num + "% less";
            };
        });

        self.cssClass = ko.computed(function() {
            if (type === "comp")
                return self.computedValue() > 0 ? "bad" : "good";
            else
                return "neutral";
        });

        self.update = function() {
            url = baseurl + ".json?last=true&" + params;
            $.getJSON(url, function(data) {
                self.value(data[0][measure]);
            });
            if (type === "comp") {
                url2 = url + "&agg2=" + agg2;
                $.getJSON(url2, function(data) {
                    self.comp(data[0][measure])
                });
            };
        };

        self.toggleChart = function(widget) {
            if (self.chart()) {
                self.chart(false);
                $('#'+widget.chartId+' svg').remove();
            }
            else {
                self.chart(true);
                if (!(self.fullSeries())) {
                    self.getMoreData();
                } else {
                    console.log("already have the data");
                }
                self.drawChart();
            }
        };

        self.getMoreData = function(widget) {
            console.log("getting more data", widget);
            /*
            url = baseurl + ".csv?" + params;
            $.get(url, function(data) {
                console.log('got ' + data.length + ' records');
                self.fullSeries(data);
            });
            */
        };

        self.drawChart = function() {
            console.log('drawing chart');

            var margin = {top: 20, right: 20, bottom: 30, left: 50},
                width = 960 - margin.left - margin.right,
                height = 300 - margin.top - margin.bottom;

            var parseDate = d3.time.format("%Y-%m-%d %X").parse;

            var x = d3.time.scale()
                .range([0, width]);

            var y = d3.scale.linear()
                .range([height, 0]);

            var xAxis = d3.svg.axis()
                .scale(x)
                .orient("bottom");

            var yAxis = d3.svg.axis()
                .scale(y)
                .orient("left");

            var line = d3.svg.line()
                .x(function(d) { return x(d.start) })
                .y(function(d) { return y(d.value) });

            var svg = d3.select('#' + self.chartId).append('svg')
                .attr("width", width + margin.left + margin.right)
                .attr("height", height + margin.top + margin.bottom)
              .append("g")
                .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

            d3.csv(baseurl + ".csv?" + params, function(error, data) {

                console.log(data);

                data.forEach(function(d) {
                    d.start = parseDate(d.start);
                    d.value = +d.value
                });

                x.domain(d3.extent(data, function(d) { return d.start; }));
                y.domain(d3.extent(data, function(d) { return d.value; }));

                svg.append("g")
                    .attr("class", "y axis")
                    .call(yAxis)
                  .append("text")
                    .attr("transform", "rotate(-90)")
                    .attr("y", 6)
                    .attr("dy", ".71em")
                    .style("text-anchor", "end")
                    .text("Value (kWh)")

                svg.append("path")
                    .datum(data)
                    .attr("class", "line")
                    .attr("d", line);
            });
        };
       
        self.update();
    };
    return Widget;
});


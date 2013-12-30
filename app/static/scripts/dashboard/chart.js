define(['knockout', 'jquery-ui'], function(ko, jqueryui) {

    var Chart = function(chartId, baseurl, params) {
        var self = this;

        self.graph = new Rickshaw.Graph.Ajax({
            element: document.querySelector("#chart" + chartId),
            width: document.querySelector("#chart" + chartId).offsetWidth,
            height: 200,
            renderer: 'line',
            dataURL: baseurl + "?series=true",
            onData: function(data) {
                var dataFormat = function(data) {
                    /* consumes a list of data and returns the x, y mapping */
                    return data.map(function(d) {
                        return { x: new Date(d.start).getTime(), y: d.value };
                    })
                };
                var dataSplit = function(data) {
                    /* consumes a JSON array of data with 'type' field
                     * and splits it into an object with indicies 'type'
                     * and values being arrays of the data of that type */
                    var result = {};
                    data.forEach(function(d) {
                        key = d.type;
                        if (key in result)
                            result[key].push(d);
                        else
                            result[key] = [d];
                    });
                    return result;
                };
                // split the data response into lists of type
                split = dataSplit(data);
                // rickshaw format each list, then add it to charting
                var chartingData = [];
                for (dataType in split) {
                    dataSeries = split[dataType];
                    chartingData.push({
                        'color': 'steelblue',
                        'name': dataType,
                        'data': dataFormat(dataSeries)
                    });
                };
                console.log(chartingData);
                return chartingData;
            },
            onComplete: function(transport) {
                var graph = transport.graph;
                var detail = new Rickshaw.Graph.HoverDetail({
                    graph: graph,
                    xFormatter: function(x) { return new Date(x).toString(); },
                    yFormatter: function(y) { return y.toFixed(1) + " kWh"; }
                });
                var slider = new Rickshaw.Graph.RangeSlider({
                    graph: graph,
                    element: document.querySelector("#slider" + chartId)
                 });
                var yAxis = new Rickshaw.Graph.Axis.Y({ graph: graph });
                yAxis.graph.update();
                spinner(false);
            }
        });

        var resize = function() {
            var padding = 10;
            var graphObj = self.graph.graph; // lol! weird properties I don't understand
            var el = graphObj.element;
            graphObj.configure({
                width: el.offsetWidth - padding,
                height: el.offsetHeight - padding
            });
            graphObj.render();
            $("#slider" + chartId).width(el.offsetWidth - padding);
        };

        window.addEventListener('resize', resize);
    };

    return Chart;

});

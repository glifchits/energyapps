define(['knockout', 'jquery-ui'], function(ko, jqueryui) {

    var Chart = function(chartId, baseurl, params) {
        var self = this;

        self.graph = new Rickshaw.Graph.Ajax({
            element: document.querySelector("#" + chartId),
            height: 200,
            renderer: 'line',
            dataURL: baseurl + ".json?" + params + "&agg=avg",
            onData: function(data) {
                var dataTransform = data.map(function(d) {
                    return {
                        x: new Date(d.start).getTime(),
                        y: d.value
                    };
                });
                return [{
                    "color": "steelblue",
                    "name": "Value",
                    "data": dataTransform
                }];
            },
            onComplete: function(transport) {
                var graph = transport.graph;
                var detail = new Rickshaw.Graph.HoverDetail({
                    graph: graph,
                    xFormatter: function(x) { return new Date(x).toDateString(); },
                    yFormatter: function(y) { return y.toFixed(1) + " kWh"; }
                });
                var slider = new Rickshaw.Graph.RangeSlider({
                    graph: graph,
                    element: document.querySelector("#slider" + chartId)
                 });
                var yAxis = new Rickshaw.Graph.Axis.Y({ graph: graph });
                yAxis.graph.update();
            },
            series: [{ name: "Value", color: "red" }]
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
        };

        window.addEventListener('resize', resize);
    };

    return Chart;

});

define(['knockout', 'jquery-ui'], function(ko, jqueryui) {
    var Chart = function(chartId, baseurl, onDataCallback) {
        var self = this;

        self.graph = new Rickshaw.Graph.Ajax({
            element: document.querySelector("#chart" + chartId),
            width: document.querySelector("#chart" + chartId).offsetWidth,
            height: 200,
            renderer: 'line',
            dataURL: baseurl + "?series=true",
            onData: function(data) {
                return onDataCallback(data);
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
                var xAxis = new Rickshaw.Graph.Axis.X({
                    graph: graph,
                    tickFormat: function(x) {
                        return new Date(x).toLocaleDateString();
                    }
                });
                xAxis.graph.update();
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

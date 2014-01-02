define(['knockout', 'jquery-ui'], function(ko, jqueryui) {

    var toMonth = function(month) {
        switch(month + 1) {
            case 1: return "January";
            case 2: return "February";
            case 3: return "March";
            case 4: return "April";
            case 5: return "May";
            case 6: return "June";
            case 7: return "July";
            case 8: return "August";
            case 9: return "September";
            case 10: return "October";
            case 11: return "November";
            case 12: return "December";
            default: "<Invalid>";
        };
    };

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
                        var date = new Date(x);
                        return toMonth(date.getUTCMonth()).substring(0,3) + ' ' + date.getUTCDate();
                    }
                });
                xAxis.graph.update();
                var yAxis = new Rickshaw.Graph.Axis.Y({
                    graph: graph,
                    tickFormat: function(y) {
                        return y + " kWh";
                    }
                });
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

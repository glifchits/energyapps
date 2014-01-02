define(['knockout', 'dashboard/chart'], function(ko, Chart) {
    var Widget = function(title, type, measure, url, chartCallback) {
        /*
         * title: string
         * type: 'abs' or 'comp'
         * measure: 'cost' or 'value'
         * url: string, '/data/...'
         */
        var self = this;
        self.title = title;
        self.chartId = self.title.replace(new RegExp(' ', 'g'), '')+Math.round(Math.random()*100);

        self.value = ko.observable(0);
        self.aggregate = ko.observable(0);

        self.text1 = "text1";
        self.text2 = "text2";

        self.displayValue = ko.computed(function() {
            return self.value().toFixed(2);
        });

        self.cssClass = ko.computed(function() {
           return "neutral";
        });

        self.update = function() {
            $.getJSON(url, function(data) {
                if (type === 'abs')
                    self.value(data[0][measure]);
                else {
                    var mapData = {};
                    data.forEach(function(d) {
                        mapData[d.type] = d;
                    });
                    self.value(mapData.value[measure]);
                    self.aggregate(mapData.aggregate[measure]);
                }
            });
        };

        self.toggleChart = function() {
            var el = $("#" + self.chartId + " .fullchart");
            if (!self.chart) {
                el.show();
                self.drawChart();
            } else if (el.css('display') !== 'none')
                el.hide();
            else
                el.show();
        };

        self.drawChart = function() {
            spinner(true, "Loading chart...");
            self.chart = new Chart( self.chartId, url, chartCallback );
        };

        self.update();
    };
    return Widget;
});


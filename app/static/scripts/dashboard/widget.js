define(['knockout', 'dashboard/chart'], function(ko, Chart) {
    var Widget = function(title, type, measure, url) {
        /*
         * title: string
         * type: 'abs' or 'comp'
         * measure: 'cost' or 'value'
         * url: string, '/data/...'
         */
        var self = this;
        self.title = title;
        self.chartId = self.title.replace(' ', '')+Math.round(Math.random()*100);

        self.value = ko.observable(0);
        self.average = ko.observable(0);

        self.text1 = "text1";
        self.text2 = "text2";

        self.displayValue = ko.computed(function() {
            if (type === 'abs' && measure === 'cost')
                return "$" + self.value().toFixed(2);
            else if (type === 'abs' && measure === 'value')
                return self.value().toFixed(1) / 1000 + " kWh";
            else if (type === 'comp') {
                var val = (self.value() - self.average()) / self.average();
                s = Math.abs(val).toFixed(2);
                s += (val > 0) ? "% more" : "% less";
                return s;
            }
        });

        self.cssClass = ko.computed(function() {
           if (type === 'comp') {
                var val = (self.value() - self.average()) / self.average();
                return (val > 0) ? "bad" : "good";
           }
           else if (type === 'abs')
               return "neutral";
        });

        self.update = function() {
            $.getJSON(url, function(data) {
                console.log('update', url, data);
                self.value(data[0][measure]);
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
            self.chart = new Chart(self.chartId, url);
        };

        self.update();
    };
    return Widget;
});


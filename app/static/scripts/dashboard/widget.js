define(['knockout'], function(ko) {
    var Widget = function(title, type, measure, baseurl, params, agg2) {
        var self = this;
        self.title = title;
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
            }
            else {
                self.chart(true);
                if (!(self.fullSeries())) {
                    self.getMoreData();
                } else {
                    console.log("already have the data");
                }
            }
        };

        self.getMoreData = function(widget) {
            console.log("getting more data", widget);
            url = baseurl + ".csv?" + params;
            $.get(url, function(data) {
                console.log('got ' + data.length + ' records');
                self.fullSeries(data);
            });
        };
        
        self.update();
    };
    return Widget;
});


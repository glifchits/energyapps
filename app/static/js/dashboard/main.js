BASE_URL = "/data/series.json"

var Widget = function(title, type, measure, params, agg2) {
    var self = this;
    self.title = title;
    self.type = type;
    self.params = params;
    self.agg2 = agg2;
    self.text1 = 'text1';
    self.text2 = 'text2';
    self.value = ko.observable(0);
    self.comp = ko.observable(0);

    self.displayValue = ko.computed(function() {
        num = self.value();
        compValue = self.comp();
        if (type === "abs") {
            if (measure === "cost")
                return "$" + num.toFixed(2);
            else
                return num.toFixed(2) + " kWh";
        }
        else {
            delta = ((num-compValue)/compValue).toFixed(2);
            if (delta > 0)
                return delta + "% more";
            else
                return delta + "% less";
        }
    });

    self.cssClass = ko.computed(function() {
        if (type === "comp")
            return self.value() > 0 ? "bad" : "good"
        else
            return "neutral"
    });

    self.update = function() {
        url = BASE_URL + "?last=true&" + params;
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
    self.update();
};

var AbsWidget = function(title, measure, params) {
    return new Widget(title, "abs", measure, params);
};

var CompWidget = function(title, measure, params, agg2) {
    agg2 = agg2 || 'avg';
    return new Widget(title, "comp", measure, params, agg2)
};

var getDateStr = function(date, dayOffset) {
    dayOffset = dayOffset || 0;
    d = new Date(date - (dayOffset * 24 * 60 * 60 * 1000));
    return d.getUTCFullYear() + '-' + 
        d.getUTCMonth() + '-' +
        d.getUTCDay();
};

var WidgetsViewModel = function() {
    var self = this;
    this.date = new Date();

    self.widgets = ko.observableArray([
        new AbsWidget("Today", "cost", "grp=day"),
        new CompWidget("Yesterday", "value", 
                       "grp=day&end=" + getDateStr(new Date(), 1))
    ]);
};

$(function() {
    ko.applyBindings(new WidgetsViewModel());
});

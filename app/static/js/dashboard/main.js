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

    self.computedValue = ko.computed(function() {
        if (!(self.comp()))
            return self.value();
        num = self.value();
        comp = self.comp();
        return (num-comp) / comp;
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
    w = new Widget(title, "abs", measure, params);
    if (measure === "cost") {
        w.text1 = "your energy use cost";
        w.text2 = "";
    }
    else {
        w.text1 = "you have used";
        w.text2 = "of energy";
    };
    return w;
};

var CompWidget = function(title, measure, params) {
    w = new Widget(title, "comp", measure, params, "avg");
    if (measure === "cost") {
        w.text1 = "your energy use cost";
        w.text2 = "than average";
    }
    else {
        w.text1 = "you used";
        w.text2 = "energy than average"
    }
    return w;
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
                       "grp=day&end=" + getDateStr(new Date(), 1)),
        new CompWidget("Last week", "cost", "grp=week"),
        new AbsWidget("This month", "value", "grp=month")
    ]);
};

$(function() {
    ko.applyBindings(new WidgetsViewModel());
});

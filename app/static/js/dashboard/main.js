
var Widget = function(title, text1, text2, params, type) {
    var self = this;
    self.title = title + ",";
    self.text1 = text1;
    self.text2 = text2;
    self.params = params;
    self.type = type;
    self.value = ko.observable();
    self.displayValue = ko.computed(function() {
        str = ''; num = self.value();
        if (self.type === "dollar") {
            str += "$";
            num = num / 100000;
        };
        str += Math.abs(num).toFixed(2);
        return str
    });
    self.cssClass = ko.computed(function() {
        return self.value() > 0 ? "bad" : "good"
    });
    self.update = function() {
        url = "/data/series.json?last=true";
        if (self.params !== '')
            url += '&' + self.params;
        $.getJSON(url, function(data) {
            self.value(data[0].cost);
            console.log(data[0].cost);
        });
    };
    self.update();
};

var WidgetsViewModel = function() {
    var self = this;

    self.widgets = ko.observableArray([
        new Widget(
            "Today", 
            "your energy use has cost",
            "so far",
            "grp=day",
            "dollar"
        ),
    ]);
};

$(function() {
    ko.applyBindings(new WidgetsViewModel());
});

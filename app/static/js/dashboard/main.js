
var Widget = function(title, text1, text2, params) {
    var self = this;
    self.title = title;
    self.text1 = ''
    self.params = params || '';
    self.value = ko.observable();
    self.displayValue = ko.computed(function() {
        return Math.abs(self.value()).toFixed(2);
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
        new Widget("Today", "grp=day")
    ]);
};

$(function() {
    ko.applyBindings(new WidgetsViewModel());
});

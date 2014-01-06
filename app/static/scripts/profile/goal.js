define(['knockout'], function(ko) {

    var Goal = function() {
        var self = this;
        self.id = ko.observable(0);
        self.target = ko.observable(0);
        self.scope = ko.observable(null);

        self.changed = ko.observable(false);

        self.name = ko.computed(function() {
            switch (self.scope()) {
                case ('week'):  return "Weekly usage";
                case ('day'):   return "Daily usage";
                case ('month'): return "Monthly usage";
                default:        return "Select a goal scope!";
            };
        });
    };
    return Goal;

});

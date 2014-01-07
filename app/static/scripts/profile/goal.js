define(['knockout'], function(ko) {

    var Goal = function() {
        var self = this;
        self.id = ko.observable(0);
        self.target = ko.observable(0);
        self.scope = ko.observable(null);

        self.computeHash = ko.computed(function() {
            /* returns a string that tries to uniquely
             * capture the current state of this object */
            var res = "" + self.id() + "-" + self.target() + self.scope();
            return res;
        });

        self.initialState = ko.observable(null);
        // when initialized, set this to the computedHash

        self.changed = function() {
            /* returns whether the object has changed since its
             * state was saved (by setting self.initialState) */
            return self.computeHash() !== self.initialState();
        };

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

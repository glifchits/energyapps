require(['./common'], function() {
    require(['knockout'], function(ko) {
        var authModel = function() {
            var self = this;
            self.name = ko.observable();
            self.email = ko.observable();
            self.pass = ko.observable();
            self.conf = ko.observable();

            self.canSubmit = ko.computed(function() {
                return self.name() && self.email() && self.pass()
                   && self.pass() === self.conf();
            });
        };

        ko.applyBindings(new authModel);
    });
});

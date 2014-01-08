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

        self.save = function() {
            var data = {};
            data['target'] = self.target();
            data['scope']  = self.scope();

            var dataList = [];
            for (var key in data) {
                var val = data[key];
                dataList.push(key + '=' + val);
            };
            var paramStr = dataList.join('&');

            url = '/data/goals';
            if (self.id() !== 0)
                url += '/' + self.id(); // add the id (modify old goal)
            url += '?' + paramStr;

            spinner(true, "Saving goal...");
            $.post(url, function(data) {
                spinner(false);
            });

            self.initialState(self.computeHash());
        };

        self.remove = function() {
            spinner(true, "Deleting goal...");
            $.post('/data/goals/' + self.id() + '/delete', function(data) {
                console.log('delete, got data', data);
                spinner(false);
            });
        };

    };
    return Goal;

});

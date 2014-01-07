define(['knockout', 'profile/goal'], function(ko, Goal) {
    var ProfileView = function() {
        var self = this;

        self.goals = ko.observableArray([]);

        self.update = function() {
            spinner(true, "Loading goals...");
            $.getJSON('/data/goals', function(goalsData) {
                console.log('updating goals');
                goalsData.forEach(function(goalData) {
                    var goalObj = new Goal();
                    goalObj.id(goalData.id);
                    goalObj.target(goalData.target);
                    goalObj.scope(goalData.scope);
                    goalObj.initialState(goalObj.computeHash());
                    self.goals.push(goalObj);
                });
                spinner(false);
            });
        };

        self.scopeOptions = ko.observableArray(['day', 'week', 'month']);
        
        self.update();

        self.addGoal = function() {
            self.goals.push(new Goal());
        };
    };

    return ProfileView;
});

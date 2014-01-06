define(['knockout', 'profile/goal'], function(ko, Goal) {
    var ProfileView = function() {
        var self = this;

        self.goals = ko.observableArray([]);

        self.update = function() {
            $.getJSON('/data/goals', function(goalsData) {
                console.log('updating goals');
                goalsData.forEach(function(goalData) {
                    var goalObj = new Goal();
                    goalObj.id(goalData.id);
                    goalObj.target(goalData.target);
                    goalObj.scope(goalData.scope);
                    self.goals.push(goalObj);
                });
            });
        };

        self.scopeOptions = ko.observableArray(['day', 'week', 'month']);
        
        self.update();
    };

    return ProfileView;
});

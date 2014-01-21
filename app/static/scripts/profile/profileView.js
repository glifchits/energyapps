define(['knockout', 'profile/goal'], function(ko, Goal) {
    var ProfileView = function() {
        var self = this;

        self.goals = ko.observableArray([]);
        self.avgMonth = 0;
        self.avgWeek = 0;

        self.update = function() {
            spinner(true, "Loading goals...");
            $.getJSON('/data/goals', function(jsonData) {
                var goalsData = jsonData.goals;
                var avgsData = jsonData.averages;

                var avgs = {};
                avgsData.forEach(function(avgData) {
                   avgs[avgData.scope] = avgData;
                });

                goalsData.forEach(function(goalData) {
                    var goalObj = new Goal();
                    goalObj.id(goalData.id);
                    goalObj.old.target = goalData.target;
                    goalObj.old.scope = goalData.scope;
                    goalObj.target(goalData.target);
                    goalObj.scope(goalData.scope);
                    goalObj.initialState(goalObj.computeHash());
                    goalObj.avgMonth = avgs.month.value;
                    goalObj.avgWeek = avgs.week.value;
                    self.goals.push(goalObj);
                });

                self.avgMonth = avgs.month.value;
                self.avgWeek = avgs.week.value;
            })
            .complete(function() {
                spinner(false)
            });
        };

        self.scopeOptions = ko.observableArray(['week', 'month']);
        
        self.update();

        self.addGoal = function() {
            goal = new Goal();
            goal.avgMonth = self.avgMonth;
            goal.avgWeek = self.avgWeek;
            self.goals.push(goal);
        };
    };

    return ProfileView;
});

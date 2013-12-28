define(['knockout', 'dashboard/widget', 'dashboard/goal'], function(ko, Widget, Goal) {
    BASE_URL = "/data/series"

    var AbsWidget = function(title, measure, params) {
        w = new Widget(title, "abs", measure, BASE_URL, params);
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
        w = new Widget(title, "comp", measure, BASE_URL, params, "avg");
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
        year = d.getUTCFullYear();
        month = d.getUTCMonth();
        day = d.getUTCDate();
        return year + '-' + ('0' + month).slice(-2) + '-' + ('0' + day).slice(-2);
    };

    var DashboardViewModel = function() {
        var self = this;
        this.date = new Date();

        self.goals = ko.observableArray([]);

        self.updateGoals = function() {
            url = '/data/goals';
            $.getJSON(url, function(goals) {
                goals.forEach(function(goal) {
                    console.log(goal);
                    var goalObj = new Goal();
                    goalObj.min(0);
                    goalObj.max(goal.end);
                    goalObj.goal((goal.value / goal.target) * goal.end);
                    goalObj.current(goal.current);
                    goalObj.titleText(goal.name);
                    self.goals.push(goalObj);
                });

            });
        };
        self.updateGoals();

        self.widgets = ko.observableArray([
            new AbsWidget("Today", "cost", "grp=day"),
            new CompWidget("Yesterday", "value", 
                           "grp=day&end=" + getDateStr(new Date(), 1)),
            new CompWidget("Last week", "cost", "grp=week"),
            new AbsWidget("This month", "value", "grp=month")
        ]);
    };

    return DashboardViewModel;
});


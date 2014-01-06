define(['knockout', 'dashboard/widget', 'dashboard/goal'], function(ko, Widget, Goal) { 
    var dataSplit = function(data) {
        /* consumes a JSON array of data with 'type' field
         * and splits it into an object with indicies 'type'
         * and values being arrays of the data of that type */
        var result = {};
        data.forEach(function(d) {
            key = d.type;
            if (key in result)
                result[key].push(d);
            else
                result[key] = [d];
        });
        return result;
    };

    var DATE = '2013-12-25';

    var TodayWidget = function() {

        var chartCallback = function(data) {
            var split = dataSplit(data);

            var valueMapper = function(d) {
                return { x: new Date(d.start).getTime(), y: d.value }
            };

            var startTime = new Date(split['value'][0]['start']).getTime();
            var aggStartTime = new Date(split['aggregate'][0]['start']).getTime();

            var aggregateMapper = function(d) {
                /* need the aggregate x-axis values to align themselves with the
                 * real axis values. compute the difference and add it as an
                 * offset */
                var originalTime = new Date(d.start).getTime();
                var time = originalTime + (startTime - aggStartTime);
                return { 
                    x: time,
                    y: d.value
                }
            };
            aggregateData = split['aggregate'].map(aggregateMapper);
            valueData = split['value'].map(valueMapper);

            var chartingData = []

            chartingData.push({
                'color': 'red',
                'name': 'Average at hour',
                'data': aggregateData
            });
            chartingData.push({
                'color': 'steelblue',
                'name': 'Usage for hour',
                'data': valueData
            });

            return chartingData;
        };

        widget = new Widget('Today', 'abs', 'cost', '/data/today?date='+DATE, chartCallback);
        var self = widget;

        self.text1 = "you have spent";
        self.text2 = "on power so far";

        self.displayValue = ko.computed(function() {
            if (!self.value())
                return '--';
            return "$" + self.value().toFixed(2);
        });

        return widget;
    };

    var YesterdayWidget = function() {

        var chartCallback = function(data) {
            split = dataSplit(data);

            formattedSeries = split['value'].map(function(d) {
                return {x: new Date(d.start).getTime(), y: d.value }
            });

            avgVal = split['aggregate'][0]['value'];
            /*
            averageLine = [{
                x: formattedSeries[0].x,
                y: avgVal
            }, {
                x: formattedSeries[formattedSeries.length - 1].x,
                y: avgVal
            }];
            */
            averageLine = formattedSeries.map(function(d) {
                return { x: d.x, y: avgVal }
            });

            return [ {
                    "name": "Average daily usage",
                    "color": "red",
                    "data": averageLine
                }, {
                    "name": "Daily Usage",
                    "color": "steelblue",
                    "data": formattedSeries
                }
            ];
        };

        widget = new Widget('Yesterday', 'comp', 'value', '/data/yesterday?date='+DATE, chartCallback);
        var self = widget;

        self.text1 = "you spent";
        self.text2 = "power than average";

        self.displayValue = ko.computed(function() {
            if (!self.value() || !self.aggregate())
                return "--";
            val = (self.value() - self.aggregate()) / self.aggregate();
            return (100 * Math.abs(val)).toFixed(1) + "% " + (val > 0 ? "more" : "less");
        });

        self.cssClass = ko.computed(function() {
            val = (self.value() - self.aggregate()) / self.aggregate();
            return val > 0 ? "bad" : "good";
        });

        return widget;
    };

    var WeeklyWidget = function() {

        var chartCallback = function(data) {
            split = dataSplit(data);

            formattedSeries = split['value'].map(function(d) {
                return {x: new Date(d.start).getTime(), y: d.value};
            });

            avgVal = split['aggregate'][0]['value'];

            averageLine = formattedSeries.map(function(d) {
                return { x: d.x, y: avgVal };
            });

            return [ {
                "name": "Average weekly usage",
                "color": "red",
                "data": averageLine
            }, {
                "name": "Weekly usage",
                "color": "steelblue",
                "data": formattedSeries
            } ];
        };

        widget = new Widget("Last 7 days", 'comp', 'value', '/data/week?date='+DATE, chartCallback);
        var self = widget;

        self.text1 = "you spent";
        self.text2 = "power than average";

        self.displayValue = ko.computed(function() {
            if (!self.value() || !self.aggregate())
                return '--';
            val = (self.value() - self.aggregate()) / self.aggregate();
            return (100 * Math.abs(val)).toFixed(1) + "% " + (val > 0 ? "more" : "less");
        });

        self.cssClass = ko.computed(function() {
            val = (self.value() - self.aggregate()) / self.aggregate();
            return val > 0 ? "bad" : "good";
        });

        return widget;
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
            new TodayWidget(),
            new YesterdayWidget(),
            new WeeklyWidget()
        ]);
    };

    return DashboardViewModel;
});


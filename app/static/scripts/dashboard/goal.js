define(['knockout'], function(ko) {

    var Goal = function() {
        var self = this;
        
        self.max = ko.observable(10);
        self.min = ko.observable(0);
        self.current = ko.observable(5);
        self.goal = ko.observable(6);
        self.titleText = ko.observable("title");
        // some unlikely to collide, arbitrary value
        self.goalId = 'goal' + Math.round(Math.random() * 10000);
        
        self.messageText = ko.computed(function() {
            if (self.goal() > self.current())
                return "slow down!";
            else
                return "on track!";
        });
    };

    window.drawGoals = function(goal) {
        var self = goal[1].children[0];

        var min = 1;
        var max = 10;
        var used = 5;
        var goal = 6;
        var messageText = 'goal message';
        var titleText = 'goal title';

        var usedPct = (used - min) / (max - min);
        var goalPct = (goal - min) / (max - min);

        var height = 30;
        var msgPadding = (height / 2.8).toFixed(1);

        var svg = d3.select(self).append("svg")
          .append('g');

        var background = svg.append("rect")
            .attr('class', 'background')
            .attr('x', 0)
            .attr('y', 0)
            .attr('height', height)

        var usedSvg = svg.append("rect")
            .attr('class', 'current')
            .attr('x', 0)
            .attr('y', 0)
            .attr('height', height)

        var goalSvg = svg.append("rect")
            .attr('class', 'goal')
            .attr('width', 4)
            .attr('y', 0)
            .attr('height', height)

        var messageSvg = svg.append("text")
            .text(messageText)
            .attr('y', height - msgPadding)

        var titleSvg = svg.append("text")
            .text(titleText)
            .attr('x', msgPadding)
            .attr('y', height - msgPadding)

        var updateChart = function() {
            width = self.offsetWidth;
            background.attr('width', width);
            goalSvg.attr('x', goalPct * width);
            usedSvg.attr('width', usedPct * width);
            msg = messageSvg[0][0];
            msgWidth = msg.offsetWidth;
            messageSvg.attr('x', width - msgWidth - msgPadding);
        };
        
        updateChart();
        $(window).resize(updateChart);

    };
    
    return Goal;

});

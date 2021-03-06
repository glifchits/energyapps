define(['knockout'], function(ko) {

    var Goal = function() {
        var self = this;
        
        self.max = ko.observable(1);
        self.min = ko.observable(0);
        self.current = ko.observable(0);
        self.goal = ko.observable(0);
        self.scope = ko.observable();
        // some unlikely to collide, arbitrary value
        self.id = 'goal' + Math.round(Math.random() * 10000);

        self.titleText = ko.computed(function() {
            switch(self.scope()) {
                case "week": return "weekly usage";
                case "month": return "monthly usage";
                default: return "undefined scope!";
            };
        });
        
        self.messageText = ko.computed(function() {
            curr = (self.current() - self.min()) / (self.max() - self.min());
            if (self.goal() > curr)
                return "slow down!";
            else
                return "on track!";
        });
    };

    window.drawGoal = function(inserted, goalObj) {
        var meterSpan = $('#' + goalObj.id);

        var self = meterSpan[0];

        var min = goalObj.min();
        var max = goalObj.max();
        var used = goalObj.current();
        var goal = goalObj.goal();
        var messageText = goalObj.messageText();
        var titleText = goalObj.titleText();

        var usedPct = (used - min) / (max - min);
        var goalPct = goal;

        var height = 30;
        var msgPadding = (height / 2.8).toFixed(1);

        var svg = d3.select(self).append("svg")
          .append('g');

        var background = svg.append("rect")
            .attr('class', 'background')
            .attr('x', 0)
            .attr('y', 0)
            .attr('height', height)

        var goalSvg = svg.append("rect")
            .attr('class', 'current')
            .attr('x', 0)
            .attr('y', 0)
            .attr('height', height)

        var usedSvg = svg.append("rect")
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
            usedSvg.attr('x', usedPct * width);
            goalSvg.attr('width', goalPct * width);
            msg = messageSvg[0][0];
            msgWidth = msg.offsetWidth;
            messageSvg.attr('x', width - msgWidth - msgPadding);
        };
        
        updateChart();
        $(window).resize(updateChart);
    };
    
    return Goal;

});

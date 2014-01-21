define(['knockout'], function(ko) {

    var Goal = function() {
        var self = this;
        
        self.max = ko.observable(10);
        self.min = ko.observable(0);
        self.current = ko.observable(5);
        self.goal = ko.observable(6);
        self.titleText = ko.observable("title text");
        // some unlikely to collide, arbitrary value
        self.id = 'goal' + Math.round(Math.random() * 10000);
        
        self.messageText = ko.computed(function() {
            if (self.goal() < self.current())
                return "slow down!";
            else
                return "on track!";
        });
    };

    window.drawGoal = function(inserted, goalObj) {
        var meterSpan = $('#' + goalObj.id);
        console.log(goalObj);

        var self = meterSpan[0];

        var min = goalObj.min();
        var max = goalObj.max();
        var used = goalObj.current();
        var goal = goalObj.goal();
        var messageText = goalObj.messageText();
        var titleText = goalObj.titleText();

        console.log('min, max, used, goal, messageText, titleText');
        console.log(min, max, used, goal, messageText, titleText);

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

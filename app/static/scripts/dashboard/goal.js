define(['knockout'], function(ko) {

    var Goal = function() {
        var self = this;
        
        self.max = ko.observable(10);
        self.min = ko.observable(0);
        self.value = ko.observable(5);
        self.goal = ko.observable(6);
        self.messageText = "message";
        self.titleText = "title";
        // some unlikely to collide, arbitrary value
        self.goalId = 'goal' + Math.round(Math.random() * 10000);
        
    };

    window.drawGoals = function(goal) {
        var self = goal[1].children[0];

        var min = parseInt(self.attributes.min.value);
        var max = parseInt(self.attributes.max.value);
        var value = parseInt(self.attributes.value.value);
        var goal = parseInt(self.attributes.goal.value);
        var messageText = self.attributes.message.value;
        var titleText = self.attributes.title.value;

        var valuePct = (value - min) / (max - min);
        var goalPct = (goal - min) / (max - min);

        var height = 26;
        var msgPadding = 7;

        var svg = d3.select(self).append("svg")
          .append('g');

        var background = svg.append("rect")
            .attr('class', 'background')
            .attr('x', 0)
            .attr('y', 0)
            .attr('height', height)

        var goal = svg.append("rect")
            .attr('class', 'goal')
            .attr('x', 0)
            .attr('y', 0)
            .attr('height', height)

        var value = svg.append("rect")
            .attr('class', 'value')
            .attr('x', 0)
            .attr('y', 0)
            .attr('height', height)

        var message = svg.append("text")
            .text(messageText)
            .attr('y', height - msgPadding)

        var title = svg.append("text")
            .text(titleText)
            .attr('x', msgPadding)
            .attr('y', height - msgPadding)

        var updateChart = function() {
            width = self.offsetWidth;
            background.attr('width', width);
            goal.attr('width', goalPct * width);
            value.attr('width', valuePct * width);
            msg = message[0][0];
            msgWidth = msg.offsetWidth;
            message.attr('x', width - msgWidth - msgPadding);
        };
        
        updateChart();
        $(window).resize(updateChart);

    };
    
    return Goal;

});

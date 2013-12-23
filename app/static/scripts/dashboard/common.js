define(['jquery-ui'], function() {

    $('#goals .meter').each(function() {
        var self = this;
        var max = parseFloat(self.attributes.max.value);
        var min = parseFloat(self.attributes.min.value);
        var value = parseFloat(self.attributes.value.value);
        var goal = parseFloat(self.attributes.goal.value);

        var valuePct = (value - min) / (max - min);
        var goalPct = (goal - min) / (max - min);

        var messageText = self.attributes.text.value;
        var titleText = self.attributes.title.value;

        var width = self.offsetWidth,
            height = 36;

        var svg = d3.select(self).append("svg")
          .append('g')

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

        msgPadding = 5;
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
            msgWidth = message[0][0].offsetWidth;
            message.attr('x', width - msgWidth);
        };

        $(window).resize(updateChart);
        updateChart();

    });

});

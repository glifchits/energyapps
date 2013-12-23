define(['jquery-ui'], function() {

    $('#goals .meter').each(function() {
        var max = parseFloat(this.attributes.max.value);
        var min = parseFloat(this.attributes.min.value);
        var value = parseFloat(this.attributes.value.value);
        var goal = parseFloat(this.attributes.goal.value);

        var valuePct = (value - min) / (max - min);
        var goalPct = (goal - min) / (max - min);

        var message = this.attributes.text.value;

        var width = 400,
            height = 36;

        var svg = d3.select(this).append("svg")
            .attr('width', width)
            .attr('height', height)
          .append('g');

        var background = svg.append("rect")
            .attr('class', 'background')
            .attr('x', 0)
            .attr('y', 0)
            .attr('width', width)
            .attr('height', height);

        var goal = svg.append("rect")
            .attr('class', 'goal')
            .attr('x', 0)
            .attr('y', 0)
            .attr('width', goalPct * width)
            .attr('height', height);

        var value = svg.append("rect")
            .attr('class', 'value')
            .attr('x', 0)
            .attr('y', 0)
            .attr('width', valuePct * width)
            .attr('height', height);

        msgPadding = 5;
        var message = svg.append("text")
            .text(message)
            .attr('x', msgPadding)
            .attr('y', height - msgPadding)

    });

});

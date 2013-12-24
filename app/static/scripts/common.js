require.config({
    baseUrl: '/static/scripts',
    paths: {
        'knockout': '/static/vendor/knockout/knockout',
        'jquery': '/static/vendor/jquery/jquery',
        'jquery-ui': '/static/vendor/jqueryui/ui/jquery-ui',
        'd3': '/static/vendor/d3/d3',
        'rickshaw': '/static/vendor/rickshaw/rickshaw'
    },
});

define(['jquery'], function($) {
    var flashDelay = 3000;

    var flashAnimate = function() {
        var messages = $('.flash ul');
        var messageChildren = messages.children();
        var height = 60; // px

        if (messageChildren.length > 0) {
            var messageIdx = -parseInt(messages.css('margin-top')) / height;
            if (messageIdx < messageChildren.length)
                messages.css('margin-top', '-=' + height);
            if (messageIdx < messageChildren.length-1)
                setTimeout(flashAnimate, flashDelay);
        };
    };

    setTimeout(flashAnimate, flashDelay);

    window.spinner = function(display) {
        var spin = $("#spinner");
        if (display) {
            spin.show();
            spin.css('opacity', 0.5);
        } else {
            spin.css('opacity', 0);
            // wait for css transition
            setTimeout(function() { spin.hide(); }, 1000);
        };
    };
});


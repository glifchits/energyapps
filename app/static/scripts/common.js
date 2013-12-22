require.config({
    baseUrl: '/static/scripts',
    paths: {
        'knockout': '/static/vendor/knockout/knockout',
        'jquery': '/static/vendor/jquery/jquery',
        'd3': '/static/vendor/d3/d3',
        'rickshaw': '/static/vendor/rickshaw/rickshaw'
    },
});

define(['jquery'], function($) {
    var flashDelay = 3000;

    var flashAnimate = function() {
        console.log('called flashAnimate');

        var messages = $('.flash ul');
        var messageChildren = messages.children();
        var height = 60; // px

        if (messageChildren.length > 0) {
            var messageIdx = -parseInt(messages.css('margin-top')) / height;
            if (messageIdx < messageChildren.length)
                messages.css('margin-top', '-=' + height);
            if (messageIdx < messageChildren.length-1) {
                console.log("   gonna invoke callback");
                setTimeout(flashAnimate, flashDelay);
            }
        };
    };

    setTimeout(flashAnimate, flashDelay);
});


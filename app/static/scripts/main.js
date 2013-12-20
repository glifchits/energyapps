require.config({
    baseUrl: '/static/scripts',
    paths: {
        'knockout': '/static/vendor/knockout/knockout',
        'jquery': '/static/vendor/jquery/jquery'
    }
});

require(['knockout', 'jquery', 'dashboard/widgetView'], function(ko, $, WidgetsViewModel) {
    ko.applyBindings(new WidgetsViewModel());
});

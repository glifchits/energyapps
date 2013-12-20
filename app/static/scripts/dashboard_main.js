require.config({
    baseUrl: '/static/scripts',
    paths: {
        'knockout': '/static/vendor/knockout/knockout',
        'jquery': '/static/vendor/jquery/jquery',
        'nv': '/static/vendor/nvd3/nv.d3',
        'd3': '/static/vendor/d3/d3'
    },
});

require(['knockout', 'jquery', 'd3', 'nv', 'dashboard/widgetView'], 
        function(ko, $, d3, nv, WidgetsViewModel) {
    ko.applyBindings(new WidgetsViewModel());
});

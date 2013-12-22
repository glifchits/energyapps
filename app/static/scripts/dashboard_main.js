require(['./common'], function(common) {
    require(['knockout', 'jquery', 'd3', 'nv', 'dashboard/widgetView'],
            function(ko, $, d3, nv, WidgetsViewModel) {
        ko.applyBindings(new WidgetsViewModel());
    });
});

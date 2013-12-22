require(['./common'], function(common) {
    require(['knockout', 'jquery', 'd3', 'rickshaw', 'dashboard/widgetView'],
            function(ko, $, d3, Rickshaw, WidgetsViewModel) {
        ko.applyBindings(new WidgetsViewModel());
    });
});

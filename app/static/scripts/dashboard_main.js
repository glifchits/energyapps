require(['./common'], function(common) {
    require(['knockout', 'd3', 'rickshaw', 'dashboard/common', 'dashboard/widgetView'],
            function(ko, d3, Rickshaw, dashCommon, WidgetsViewModel) {
        ko.applyBindings(new WidgetsViewModel());
    });
});

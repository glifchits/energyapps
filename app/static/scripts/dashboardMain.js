require(['./common'], function(common) {
    require(['knockout', 'd3', 'rickshaw', 'dashboard/common', 'dashboard/widgetView'],
            function(ko, d3, Rickshaw, dashCommon, WidgetsViewModel) {

        ko.applyBindings(new WidgetsViewModel());

        var updateEUI = function() {
            $.getJSON('/data/last_date', function(data) {
                var date = new Date(data);
                var now = new Date();
                var hoursDiff = (now - date) / (1000 * 60 * 60);
                if (hoursDiff > 1) {
                    url = '/eui?start=' + (date.getTime() / 1000);
                    spinner(true);
                    $.getJSON(url, function(data) {
                        console.log('received eui', data);
                    });
                    spinner(false);
                };
            });
        };
        updateEUI();

    });
});

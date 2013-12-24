require(['./common'], function(common) {
    require(['knockout', 'd3', 'rickshaw', 'dashboard/common', 'dashboard/widgetView'],
            function(ko, d3, Rickshaw, dashCommon, WidgetsViewModel) {

        var updateEUI = function() {
            $.getJSON('/data/last_date', function(data) {
                var date = new Date(data);
                console.debug('last update date is', date);
                var now = new Date();
                var hoursDiff = (now - date) / (1000 * 60 * 60);
                if (hoursDiff > 0) {
                    url = '/eui?start=' + date.getTime();
                    spinner(true);
                    console.log("getting the EUI");
                    $.getJSON(url, function(data) {
                        console.log(data);
                    });
                    spinner(false);
                };
            });
        };
        updateEUI();

        ko.applyBindings(new WidgetsViewModel());
    });
});

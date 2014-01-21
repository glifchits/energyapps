require(['./common'], function(common) {
    require(['knockout', 'd3', 'rickshaw', 'dashboard/common', 'dashboard/dashboardView'],
            function(ko, d3, Rickshaw, dashCommon, DashboardViewModel) {

        ko.applyBindings(new DashboardViewModel());

        var updateEUI = function() {
            $.getJSON('/data/last_date', function(data) {
                var date = new Date(data);
                var now = new Date();
                var hoursDiff = (now - date) / (1000 * 60 * 60);
                if (hoursDiff > 1) {
                    url = '/eui?start=' + (date.getTime() / 1000);
                    spinner(true, "Updating energy data...");
                    $.get(url, function(data) {
                        console.log('received eui', data);
                    })
                    .complete(function(data) {
                        spinner(false);
                    });
                };
            });
        };
        updateEUI();

    });
});

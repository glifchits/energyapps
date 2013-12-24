require(['./common'], function(common) {
    require([], function() {

        var updateEUI = function() {
            console.log("getting the EUI");
            $.getJSON('/eui', function(data) {
                console.log(data);
            });
        };
        updateEUI();

    });
});

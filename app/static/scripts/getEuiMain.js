require(['./common'], function(common) {
    require([], function() {

        var updateEUI = function() {
            $('#eui-continue .continue').text("Loading... Please wait")
            $.get('/eui', function(data) {
                console.log(data);
                $('#eui-continue .continue')
                    .text('Continue')
                    .prop('disabled', false);
            });
        };
        updateEUI();

    });
});

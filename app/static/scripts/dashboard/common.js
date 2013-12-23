define(['jquery-ui'], function() {

    $('#goals .meter').each(function() {
        var max = parseFloat(this.attributes.max.value);
        var min = parseFloat(this.attributes.min.value);
        var value = parseFloat(this.attributes.value.value);
        var pct = (value - min) / (max - min) * 100;
        $(this).progressbar({
            value: pct
        });
    });

});

// Generated by CoffeeScript 1.6.3
(function() {
  var updateEUI;

  updateEUI = function() {
    var spinner;
    console.log('getting eui');
    spinner = $('#spinner');
    spinner.css('opacity', 0.8);
    return $.get('/eui', function(data) {
      console.log('got data');
      console.log(data);
      spinner.css('opacity', 0);
      return console.log('done getting eui');
    });
  };

  $('#refresh-eui').click(function() {
    console.log('would have called update eui');
    return updateEUI();
  });

}).call(this);

updateEUI = () ->
  console.log 'getting eui'

  spinner = $('#spinner')
  spinner.css('opacity', 0.8)

  $.get '/eui', (data) ->
    console.log 'got data'
    console.log data
    spinner.css('opacity', 0)
    console.log 'done getting eui'


$('#refresh-eui').click ->
  console.log 'would have called update eui'
  updateEUI()

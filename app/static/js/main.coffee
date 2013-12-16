updateEUI = () ->
  console.log 'getting eui'
  $.get '/eui', (data) ->
    console.log 'got data'
    console.log data
    console.log 'done getting eui'

$('#refresh-eui').click ->
  console.log 'would have called update eui'
  updateEUI()

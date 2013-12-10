utils = require "./utils"

ctx = document.getElementById('chart').getContext('2d')

drawChart = (key = 'cost') ->
  $.getJSON '/data/hour', (response) ->
    readings = (key) ->
      rs = (response[i] for i in [0..23])
      rs.map (r) -> (d[key] for d in r)

    normalizedDataset = (key) ->
      allData = readings(key)
      (utils.average(dataset) for dataset in allData)

    selectedKeys = () ->
      (x.name for x in $('#chartKeys > input') when x.checked)

    getDataset = (key) -> {
        fillColor: utils.randomRGB(0.5)
        data: normalizedDataset(key)
      }

    data =
      labels: ("#{hr}:00" for hr in [0..23])
      datasets: (getDataset(key) for key in selectedKeys())

    chart = new Chart(ctx).Radar(data)


drawChart()
$('#chartKeys > input').click(drawChart)

average = (set) ->
  total = set.reduce (x, y) -> x + y
  total / set.length

max = (set) -> 
  Math.max.apply @, set

# thanks to http://www.paulirish.com/2009/random-hex-color-code-snippets/
randomHex = () ->
  "##{Math.floor(Math.random() * 16777215).toString(16)}"

randomRGB = (alpha = 1) ->
  r = parseInt Math.random() * 255
  g = parseInt Math.random() * 255
  b = parseInt Math.random() * 255
  "rgba(#{r},#{g},#{b},#{alpha})"

ctx = document.getElementById('chart').getContext('2d')

drawChart = (key = 'cost') ->
  $.getJSON '/data/hour', (response) ->
    readings = (key) ->
      rs = (response[i] for i in [0..23])
      rs.map (r) -> (d[key] for d in r)

    normalizedDataset = (key) ->
      allData = readings(key)
      (average(dataset) for dataset in allData)

    selectedKeys = () ->
      (x.name for x in $('#chartKeys > input') when x.checked)

    getDataset = (key) -> {
        fillColor: randomRGB(0.5)
        data: normalizedDataset(key)
      }

    data =
      labels: ("#{hr}:00" for hr in [0..23])
      datasets: (getDataset(key) for key in selectedKeys())

    chart = new Chart(ctx).Radar(data)


drawChart()
$('#chartKeys > input').click(drawChart)

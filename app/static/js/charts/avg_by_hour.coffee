$.getJSON '/data/hour', (response) ->
  console.log response

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

  readings = (key) ->
    rs = (response[i] for i in [0..23])
    rs.map (r) -> (d[key] for d in r)

  data =
    labels: ("#{hr}:00" for hr in [0..23])
    datasets:
      [
        {
          fillColor: randomRGB(0.5)
          data: 
            readings.map (r) -> 
              dataset = (d.cost for d in r)
              average(dataset)#/ max(dataset)
        }
        {
          fillColor: randomRGB(0.5)
          data:
            readings.map (r) ->
              dataset = (d.value for d in r)
              average(dataset)# / max(dataset)
        }
      ]

  console.log data

  ctx = document.getElementById('chart').getContext('2d')
  chart = new Chart(ctx).Radar(data)
  null

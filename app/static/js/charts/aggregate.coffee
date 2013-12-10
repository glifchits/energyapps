ctx = document.getElementById('chart').getContext('2d')

drawChart = (cost, value) ->
  agg = utils.urlParameters 'agg'
  grp = utils.urlParameters 'grp'
  start = utils.urlParameters 'start'
  end = utils.urlParameters 'end'
  url = "/data/aggregate.json?agg=#{agg}&grp=#{grp}"
  if start?
    url += "&start=#{start}"
  if end?
    url += "&end=#{end}"

  $.getJSON url, (response) ->
    labels = response.map (grpData) -> grpData[grp]
    datasets = []
    if cost
      datasets.push
        fillColor: utils.randomRGB(0.5)
        data: response.map (grpData) -> grpData.cost
    if value
      datasets.push
        fillColor: utils.randomRGB(0.5)
        data: response.map (grpData) -> grpData.value

    chart = new Chart(ctx).Line({
      labels: labels
      datasets: datasets
    })

drawChart(true, true)


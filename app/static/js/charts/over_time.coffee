$.getJSON '/data/readings', (response) =>
  data = 
    labels: (d.start for d in response by 24)
    datasets: [
      fillColor : "rgba(220,220,220,0.5)"
      strokeColor : "rgba(220,220,220,1)"
      pointColor : "rgba(220,220,220,1)"
      pointStrokeColor : "#fff"
      data: (d.cost for d in response by 24)

  console.log data

  ctx = document.getElementById('chart').getContext('2d')
  chart = new Chart(ctx).Line(data)
  null

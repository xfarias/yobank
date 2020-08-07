                             /* globals Chart:false, feather:false */

(function () {
  'use strict'

  feather.replace()

  var user = username

  const name = user.map(({username}) => username)
  const cred =  user.map(({credit}) => credit)
  const debt =  user.map(({debt}) => debt)


  var ctx = document.getElementById("myChart").getContext('2d');
  var myChart = new Chart(ctx, {
type: 'bar',
data: {
labels: ["Crédito", "Débito"],
datasets: [{
data: [cred, debt],
backgroundColor: [
'rgba(255, 99, 132, 0.2)',
'rgba(54, 162, 235, 0.2)'

],
borderColor: [
'rgba(255,99,132,1)',
'rgba(54, 162, 235, 1)'
],
borderWidth: 1
}]
},
options: {
scales: {
yAxes: [{
ticks: {
beginAtZero: true
}
}]
}
}
})
}())





var endpoint = '/api/trip/cat/'
$.ajax({
    method: "GET",
    url: endpoint,
    success: function(data){
        categories = data.categories
        lt = data.lt
        ot = data.ot
        lenged = data.legend
        setChartEmpTrip()
    },
    error: function(error_data){
        console.log("error")
        console.log(error_data)
    }
})

function setChartEmpTrip(){

Highcharts.chart('setChartEmpTrip', {
    chart: {
        type: 'bar'
    },
    title: {
        text: lenged
    },
    xAxis: {
        categories: categories
    },
    series: [
        { name: 'Local Field Trip', data: lt }, 
        { name: 'Overseas Travel', data: ot },
    ],
    credits: {
        enabled: false
    }
});
}

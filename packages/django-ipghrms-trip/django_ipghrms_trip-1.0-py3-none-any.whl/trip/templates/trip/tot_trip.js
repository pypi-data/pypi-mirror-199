var endpoint = '/api/trip/cat/tot/'
$.ajax({
    method: "GET",
    url: endpoint,
    success: function(data){
        obj = data.obj
        legend = data.label
        setTripTotal()
    },
    error: function(error_data){
        console.log("error")
        console.log(error_data)
    }
})

function setTripTotal(){


    Highcharts.chart('allTripTot_chart', {
        colors: ['#01BAF2', '#71BF45', '#FAA74B', '#B37CD2', '#d42c06', '#dbde23', '#68d9d7'],
    chart: {
        type: 'pie'
    },
    accessibility: {
        point: {
            valueSuffix: '%'
        }
    },
    title: {
        text: legend
    },
    tooltip: {
        formatter: function () {
            return this.point.name + ': ' + this.y;
        }
    },
    plotOptions: {
        pie: {
            allowPointSelect: true,
            cursor: 'pointer',
            dataLabels: {
                enabled: true,
                formatter: function () {
                    return this.point.name + ': ' + this.y;
                }
            },
            showInLegend: true
        }
    },
    credits: {
        enabled: false
  },
    series: [{
        name: 'Registrations',
        colorByPoint: true,
        innerSize: '75%',
        data: obj
    }]
    });
}


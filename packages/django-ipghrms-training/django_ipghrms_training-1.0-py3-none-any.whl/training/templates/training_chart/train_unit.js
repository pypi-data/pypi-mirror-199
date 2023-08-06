var endpoint = '/api/training/unit/'
$.ajax({
    method: "GET",
    url: endpoint,
    success: function(data){
        obj = data.obj
        legend = data.label
        setTrainingUnit()
        console.log(data)
    },
    error: function(error_data){
        console.log("error")
        console.log(error_data)
    }
})

function setTrainingUnit(){
    const chart = new Highcharts.Chart({
        chart: {
            renderTo: 'tunit_data',
            type: 'column',
            options3d: {
                enabled: true,
                alpha: 15,
                beta: 15,
                depth: 50,
                viewDistance: 25
            }
        },
        xAxis: {
            categories: legend
        },
        yAxis: {
            title: {
                enabled: false
            }
        },
        tooltip: {
            headerFormat: '<b>{point.key}</b><br>',
            pointFormat: 'Total Funsionario: {point.y}'
        },
        title: {
            text: 'DISTRIBUISAUN FUNSIONARIO TUIR FORMASAUN BASEIA BA DIVIZAUN'
        },
        legend: {
            enabled: false
        },
        plotOptions: {
            series: {
                borderWidth: 0,
                dataLabels: {
                    enabled: true,
                    format: '{point.y}'
                }
            }
        },
        credits: {
            enabled: false
      },
        series: [{
            data: obj,
            colorByPoint: true
        }]
    });
    


}







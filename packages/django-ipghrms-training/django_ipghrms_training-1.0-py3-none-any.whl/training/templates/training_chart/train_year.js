
var endpoint = '/api/training/year/'
$.ajax({
    method: "GET",
    url: endpoint,
    success: function(data){
        obj = data.obj
        legend = data.label
        legend2 = data.legend
        setEmpTrainingYear()
    },
    error: function(error_data){
        console.log("error")
        console.log(error_data)
    }
})


function setEmpTrainingYear(){
    const chart = new Highcharts.Chart({
        chart: {
            renderTo: 'tyear_data',
            type: 'column',
            options3d: {
                enabled: true,
                alpha: 0,
                beta: 0,
                depth: 6,
                viewDistance: 50
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
            text: legend2
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
    
    function showValues() {
        document.getElementById('alpha-value').innerHTML = chart.options.chart.options3d.alpha;
        document.getElementById('beta-value').innerHTML = chart.options.chart.options3d.beta;
        document.getElementById('depth-value').innerHTML = chart.options.chart.options3d.depth;
    }
    
    // Activate the sliders
    document.querySelectorAll('#sliders input').forEach(input => input.addEventListener('input', e => {
        chart.options.chart.options3d[e.target.id] = parseFloat(e.target.value);
        showValues();
        chart.redraw(false);
    }));
    
    showValues();


}





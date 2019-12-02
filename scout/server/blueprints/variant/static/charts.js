function pieChart(series, rank, score, cadd) {

Highcharts.chart('rank_pie_chart', {
    chart: {
        type: 'pie'
    },
    title: {
        text: `Rank ${rank}`
    },
    subtitle: {
        text: `Rank Score ${score}, CADD score ${cadd}`
    },
    plotOptions: {
        series: {
            dataLabels: {
                enabled: true,
                format: '{point.name}: score {point.y}'
            }
        }
    },
    tooltip: {
        headerFormat: '<span style="font-size:11px">{series.name}</span><br>',
        pointFormat: '<span style="color:{point.color}">{point.name}</span>: <b>Score {point.y}</b><br/>'
    },
    series: [
        {
            name: "Rank Score Category",
            colorByPoint: true,
            data: series
        }
    ]
    }
  );
}
window.onload = function () {
    pieChartDraw();
    document.getElementById('legend-div').innerHTML = window.pieChart.generateLegend();
}

let pieChartData = {
    labels: ['삼성전자', '호텔신라', 'LG화학', '네이버', '카카오', '라인'],
    datasets: [{
        data: [95, 12, 13, 7, 13, 10],
        backgroundColor: ['rgb(255, 99, 132)', 'rgb(255, 159, 64)', 'rgb(255, 205, 86)', 'rgb(75, 192, 192)', 'rgb(54, 162, 235)', 'rgb(153, 102, 255)']
    }]
};

let pieChartDraw = function () {
    let ctx = document.getElementById('pieChartCanvas').getContext('2d');

    window.pieChart = new Chart(ctx, {
        type: 'pie',
        data: pieChartData,
        options: {
            responsive: false,
            legend: {
                display: false
            },
            legendCallback: customLegend
        }
    });
};

let customLegend = function (chart) {
    let ul = document.createElement('ul');
    let color = chart.data.datasets[0].backgroundColor;

    chart.data.labels.forEach(function (label, index) {
        ul.innerHTML += `<li><span style="background-color: ${color[index]}"></span>${label}</li>`;
    });

    return ul.outerHTML;
};
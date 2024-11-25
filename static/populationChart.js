// Function to update the population chart
function updateChart(years, populations) {
    if (window.populationChart) {
        const reversedYears = [...years].reverse();
        const reversedPopulations = [...populations].reverse();

        // Duplicate the data point if there is only one
        if (reversedPopulations.length === 1) {
            reversedPopulations.push(reversedPopulations[0]);
            reversedYears.push(reversedYears[0]);
        }

        // Update chart data
        window.populationChart.data.labels = reversedYears;
        window.populationChart.data.datasets[0].data = reversedPopulations;

        // Ensure y-axis starts at 0 and update the chart
        window.populationChart.options.scales.yAxes[0].ticks.min = 0;
        window.populationChart.update();
    }
}

// Initial setup of the population chart
const ctx = document.getElementById('acquisitions').getContext('2d');
window.populationChart = new Chart(ctx, {
    type: 'line',
    data: {
        labels: [],
        datasets: [{
            label: 'Population Over Time',
            data: [],
            borderColor: 'rgb(75, 192, 192)',
            tension: 0.1
        }]
    },
    options: {
        scales: {
            yAxes: [{
                ticks: {
                    beginAtZero: true,
                    min: 0
                }
            }]
        }
    }
});

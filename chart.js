// Initialize chart data
let chartData = {
    labels: [],
    datasets: [{
        label: 'Heart Rate (BPM)',
        data: [],
        borderColor: '#ff6384',
        backgroundColor: 'rgba(255, 99, 132, 0.1)',
        borderWidth: 2,
        fill: true,
        tension: 0.4
    }, {
        label: 'Blood Oxygen Level (%)',
        data: [],
        borderColor: '#36a2eb',
        backgroundColor: 'rgba(54, 162, 235, 0.1)',
        borderWidth: 2,
        fill: true,
        tension: 0.4
    }]
};

// Chart configuration
const chartConfig = {
    type: 'line',
    data: chartData,
    options: {
        responsive: true,
        maintainAspectRatio: false,
        animation: {
            duration: 750,
            easing: 'linear'
        },
        scales: {
            x: {
                type: 'time',
                time: {
                    unit: 'second',
                    displayFormats: {
                        second: 'HH:mm:ss'
                    }
                },
                title: {
                    display: true,
                    text: 'Time'
                }
            },
            y: {
                beginAtZero: false,
                title: {
                    display: true,
                    text: 'Value'
                }
            }
        },
        plugins: {
            title: {
                display: true,
                text: 'Real-time Patient Vitals Monitor',
                font: {
                    size: 16
                }
            },
            legend: {
                position: 'top'
            }
        }
    }
};

let chart;

// Initialize the chart when the DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    const ctx = document.getElementById('liveChart').getContext('2d');
    chart = new Chart(ctx, chartConfig);
    startUpdatingChart();
});

// Function to generate realistic vital signs data
function generateVitalSigns() {
    return {
        heartRate: Math.floor(Math.random() * (95 - 65) + 65), // Normal heart rate range: 65-95 BPM
        oxygenLevel: Math.floor(Math.random() * (100 - 95) + 95) // Normal oxygen level range: 95-100%
    };
}

// Function to update the chart with new data
function updateChart() {
    const now = new Date();
    const vitals = generateVitalSigns();

    // Add new data points
    chartData.labels.push(now);
    chartData.datasets[0].data.push(vitals.heartRate);
    chartData.datasets[1].data.push(vitals.oxygenLevel);

    // Remove old data points to keep the chart moving
    if (chartData.labels.length > 30) {
        chartData.labels.shift();
        chartData.datasets.forEach(dataset => dataset.data.shift());
    }

    // Update the chart
    chart.update('quiet');

    // Update current values display
    document.getElementById('currentHeartRate').textContent = vitals.heartRate;
    document.getElementById('currentOxygenLevel').textContent = vitals.oxygenLevel;
}

// Start updating the chart
function startUpdatingChart() {
    // Update every 1 second
    setInterval(updateChart, 1000);
} 
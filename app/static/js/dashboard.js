// Dashboard JavaScript

$(document).ready(function() {
    // Initialize charts
    if (document.getElementById('yieldChart')) {
        initYieldChart();
    }
});

function initYieldChart() {
    const ctx = document.getElementById('yieldChart').getContext('2d');
    new Chart(ctx, {
        type: 'line',
        data: {
            labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
            datasets: [{
                label: 'Predicted Yield',
                data: [4.2, 4.5, 4.8, 5.0, 4.7, 4.3],
                borderColor: '#198754',
                backgroundColor: 'rgba(25, 135, 84, 0.1)',
                tension: 0.4,
                fill: true
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'top',
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    title: {
                        display: true,
                        text: 'Yield (tons/acre)'
                    }
                }
            }
        }
    });
}
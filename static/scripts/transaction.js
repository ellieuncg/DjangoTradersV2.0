// Ensure the script runs only when the page is fully loaded
document.addEventListener("DOMContentLoaded", () => {
    // Define the chart context
    const ctx = document.getElementById('transactionChart').getContext('2d');

    // Example Chart.js configuration
    const transactionChart = new Chart(ctx, {
        type: 'bar', // Bar chart type
        data: {
            labels: [], // Labels will be dynamically fetched
            datasets: [
                {
                    label: 'Revenue ($)',
                    data: [], // Data will be dynamically fetched
                    backgroundColor: 'rgba(75, 192, 192, 0.2)',
                    borderColor: 'rgba(75, 192, 192, 1)',
                    borderWidth: 1,
                },
            ],
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    display: true,
                },
            },
            scales: {
                x: {
                    title: {
                        display: true,
                        text: 'Categories',
                    },
                },
                y: {
                    title: {
                        display: true,
                        text: 'Revenue ($)',
                    },
                },
            },
        },
    });

    // Fetch data and update the chart
    fetch('/api/transaction-dashboard-data/')
        .then((response) => response.json())
        .then((data) => {
            transactionChart.data.labels = data.labels;
            transactionChart.data.datasets[0].data = data.revenue;
            transactionChart.update();
        })
        .catch((error) => console.error('Error fetching transaction data:', error));
});

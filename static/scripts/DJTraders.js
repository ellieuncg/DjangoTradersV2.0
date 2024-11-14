console.log('DJTraders.js loading...');

document.addEventListener('DOMContentLoaded', () => {
    console.log('Document ready in DJTraders.js');
    setupCustomerDashboardTabs();
});

const chartInstances = {};

function setupCustomerDashboardTabs() {
    const tabButtons = document.querySelectorAll('.customer-tab-button');
    const tabContents = document.querySelectorAll('.customer-tab-content');

    tabButtons.forEach(button => {
        button.addEventListener('click', () => {
            // Remove active class from all buttons and contents
            tabButtons.forEach(btn => btn.classList.remove('active'));
            tabContents.forEach(content => content.classList.remove('active'));

            // Add active class to the clicked button and corresponding content
            button.classList.add('active');
            const content = document.getElementById(button.dataset.tab);
            if (content) {
                content.classList.add('active');

                // Destroy any existing chart for this tab before initializing
                destroyChart(button.dataset.tab);

                // Initialize the chart for the active tab
                initializeChartForTab(button.dataset.tab);
            }
        });
    });
}

function initializeChartForTab(tabId) {
    console.log(`Initializing chart for tab: ${tabId}`);
    let ctx;

    if (tabId === 'tab-annual-overview') {
        ctx = document.getElementById('annualSalesChart').getContext('2d');
        chartInstances[tabId] = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: yearlyOrders,
                datasets: [{
                    label: 'Revenue',
                    data: yearlyRevenue,
                    backgroundColor: 'rgba(82, 103, 84, 0.6)',
                    borderColor: 'rgba(82, 103, 84, 1)',
                    borderWidth: 1
                }]
            },
            options: { scales: { y: { beginAtZero: true } } }
        });
    } else if (tabId === 'tab-top-products') {
        ctx = document.getElementById('topProductsChart').getContext('2d');
        chartInstances[tabId] = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: topProductsLabels,
                datasets: [{
                    label: 'Revenue',
                    data: topProductsData,
                    backgroundColor: 'rgba(179, 157, 157, 0.6)',
                    borderColor: 'rgba(82, 103, 84, 1)',
                    borderWidth: 1
                }]
            },
            options: { scales: { y: { beginAtZero: true } } }
        });
    } else if (tabId === 'tab-bottom-products') {
        ctx = document.getElementById('bottomProductsChart').getContext('2d');
        chartInstances[tabId] = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: bottomProductsLabels,
                datasets: [{
                    label: 'Revenue',
                    data: bottomProductsData,
                    backgroundColor: 'rgba(157, 179, 207, 0.6)',
                    borderColor: 'rgba(82, 103, 84, 1)',
                    borderWidth: 1
                }]
            },
            options: { scales: { y: { beginAtZero: true } } }
        });
    } else if (tabId === 'tab-category-analysis') {
        ctx = document.getElementById('categorySalesChart').getContext('2d');
        chartInstances[tabId] = new Chart(ctx, {
            type: 'pie',
            data: {
                labels: topCategoriesLabels,
                datasets: [{
                    label: 'Quantity Purchased',
                    data: topCategoriesData,
                    backgroundColor: [
                        'rgba(82, 103, 84, 0.6)',
                        'rgba(179, 207, 157, 0.6)',
                        'rgba(179, 157, 157, 0.6)',
                        'rgba(157, 179, 207, 0.6)'
                    ],
                    borderColor: 'rgba(255, 255, 255, 1)',
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false
            }
        });
    }
}

function destroyChart(tabId) {
    if (chartInstances[tabId]) {
        chartInstances[tabId].destroy();
        delete chartInstances[tabId];
    }
}

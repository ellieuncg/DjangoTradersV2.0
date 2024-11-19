console.log("DJTraders.js is loaded and running");

document.addEventListener('DOMContentLoaded', () => {
    console.log('Document ready in DJTraders.js');
    setupSalesDashboardTabs();
    setupFilterForm();
    // Initialize the default active tab's chart
    const activeTab = document.querySelector('.sales-tab-button.active');
    if (activeTab) {
        initializeChartForTab(activeTab.dataset.tab);
    }
});

// Set up filter form functionality
function setupFilterForm() {
    // Handle sales dashboard filter form
    const filterForm = document.getElementById('filterForm');
    if (filterForm) {
        const yearSelect = filterForm.querySelector('.year-select');
        const productSelect = filterForm.querySelector('.product-select');
        
        // Handle both year and product selection changes
        if (yearSelect) {
            yearSelect.addEventListener('change', () => filterForm.submit());
        }
        if (productSelect) {
            productSelect.addEventListener('change', () => filterForm.submit());
        }
    }
}

function setupSalesDashboardTabs() {
    const tabButtons = document.querySelectorAll('.sales-tab-button');
    const tabContents = document.querySelectorAll('.sales-tab-content');

    tabButtons.forEach(button => {
        button.addEventListener('click', () => {
            // Remove active class from all buttons and contents
            tabButtons.forEach(btn => btn.classList.remove('active'));
            tabContents.forEach(content => content.classList.remove('active'));

            // Add active class to clicked button and corresponding content
            button.classList.add('active');
            const content = document.getElementById(button.dataset.tab);
            if (content) {
                content.classList.add('active');
                initializeChartForTab(button.dataset.tab);
            }
        });
    });
}

function initializeChartForTab(tabId) {
    console.log(`Initializing chart for tab: ${tabId}`);
    
    // Clear any existing chart
    const chartId = getChartIdForTab(tabId);
    const existingChart = Chart.getChart(chartId);
    if (existingChart) {
        existingChart.destroy();
    }

    switch(tabId) {
        case 'tab-annual-overview':
            createAnnualOverviewChart();
            break;
        case 'tab-top-products':
            createTopProductsChart();
            break;
        case 'tab-bottom-products':
            createBottomProductsChart();
            break;
        case 'tab-category-analysis':
            createCategoryAnalysisChart();
            break;
    }
}

function getChartIdForTab(tabId) {
    const chartIds = {
        'tab-annual-overview': 'annualSalesChart',
        'tab-top-products': 'topProductsChart',
        'tab-bottom-products': 'bottomProductsChart',
        'tab-category-analysis': 'categorySalesChart',
    };
    return chartIds[tabId];
}

// Sales Dashboard Charts
function createAnnualOverviewChart() {
    const ctx = document.getElementById('annualSalesChart')?.getContext('2d');
    if (!ctx) return;

    new Chart(ctx, {
        type: 'line',
        data: {
            labels: annualSalesLabels,
            datasets: [{
                label: 'Monthly Revenue',
                data: annualSalesData,
                borderColor: 'rgb(82, 103, 84)',
                backgroundColor: 'rgba(82, 103, 84, 0.1)',
                tension: 0.4,
                fill: true
            }]
        },
        options: getChartOptions('currency', 'Monthly Sales Revenue')
    });
}

function createTopProductsChart() {
    const ctx = document.getElementById('topProductsChart')?.getContext('2d');
    if (!ctx) return;

    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: topProductsLabels,
            datasets: [{
                label: 'Revenue',
                data: topProductsData,
                backgroundColor: 'rgba(82, 103, 84, 0.7)',
                borderColor: 'rgb(82, 103, 84)',
                borderWidth: 1
            }]
        },
        options: {
            ...getChartOptions('currency', 'Top Products by Revenue'),
            indexAxis: 'y',
        }
    });
}

function createBottomProductsChart() {
    const ctx = document.getElementById('bottomProductsChart')?.getContext('2d');
    if (!ctx) return;

    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: bottomProductsLabels,
            datasets: [{
                label: 'Revenue',
                data: bottomProductsData,
                backgroundColor: 'rgba(103, 82, 84, 0.7)',
                borderColor: 'rgb(103, 82, 84)',
                borderWidth: 1
            }]
        },
        options: {
            ...getChartOptions('currency', 'Bottom Products by Revenue'),
            indexAxis: 'y',
        }
    });
}

function createCategoryAnalysisChart() {
    const ctx = document.getElementById('categorySalesChart')?.getContext('2d');
    if (!ctx) return;

    new Chart(ctx, {
        type: 'pie',
        data: {
            labels: categorySalesLabels,
            datasets: [{
                data: categorySalesData,
                backgroundColor: [
                    'rgba(82, 103, 84, 0.8)',
                    'rgba(103, 82, 84, 0.8)',
                    'rgba(84, 103, 82, 0.8)',
                    'rgba(123, 82, 84, 0.8)'
                ]
            }]
        },
        options: {
            ...getChartOptions('currency', 'Category Sales Distribution'),
            plugins: {
                legend: {
                    position: 'right'
                }
            }
        }
    });
}

function getChartOptions(type, title = '') {
    const baseOptions = {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
            legend: {
                position: 'bottom',
                labels: {
                    boxWidth: 20,
                    padding: 15
                }
            },
            title: {
                display: !!title,
                text: title,
                padding: {
                    top: 10,
                    bottom: 10
                }
            }
        },
        layout: {
            padding: {
                top: 10,
                right: 15,
                bottom: 20,
                left: 15
            }
        }
    };

    if (type === 'currency') {
        return {
            ...baseOptions,
            scales: {
                y: {
                    beginAtZero: true,
                    ticks: {
                        callback: value => '$' + value.toLocaleString()
                    }
                }
            }
        };
    }

    return baseOptions;
}

// Archive functionality
function archiveRecord(type, id) {
    const url = `/DjTraders/${type}/${id}/archive/`;
    const csrfToken = getCookie('csrftoken');

    fetch(url, {
        method: 'POST',
        headers: {
            'X-CSRFToken': csrfToken,
            'Accept': 'application/json'
        }
    })
    .then(response => {
        if (response.status === 401 || response.status === 403) {
            console.warn("Unauthorized request, redirecting to login.");
            window.location.href = '/DjTraders/accounts/login/';
        }
        return response.json();
    })
    .then(data => {
        if (data && data.status === 'archived') {
            console.log(`${type} archived successfully:`, data.message);
            window.location.reload();
        }
    })
    .catch(error => console.error('Error during archive request:', error));
}

// CSRF token helper function
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

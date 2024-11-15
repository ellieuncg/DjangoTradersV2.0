console.log("DJTraders.js is loaded and running");

document.addEventListener('DOMContentLoaded', () => {
    console.log('Document ready in DJTraders.js');
    setupCustomerDashboardTabs();
    setupFilterForm();
    // Initialize the default active tab's chart
    const activeTab = document.querySelector('.customer-tab-button.active');
    if (activeTab) {
        initializeChartForTab(activeTab.dataset.tab);
    }
});

// Set up filter form functionality
function setupFilterForm() {
    const filterForm = document.getElementById('customerFilterForm');
    if (filterForm) {
        const clearButton = filterForm.querySelector('.btn-clear');
        const inputs = filterForm.querySelectorAll('input[type="text"], select');
        const countrySelect = document.getElementById('country');

        if (clearButton) {
            clearButton.addEventListener('click', (e) => {
                e.preventDefault();
                console.log("Clear button clicked");
                inputs.forEach(input => input.value = '');
                const letterInput = filterForm.querySelector('input[name="letter"]');
                if (letterInput) letterInput.remove();
                filterForm.submit();
            });
        }

        if (countrySelect) {
            countrySelect.addEventListener('change', () => {
                console.log('Country changed to:', countrySelect.value);
                filterForm.submit();
            });
        }
    }

    const yearSelect = document.querySelector('.year-select');
    if (yearSelect) {
        yearSelect.addEventListener('change', () => {
            yearSelect.closest('form').submit();
        });
    }
}

function setupCustomerDashboardTabs() {
    const tabButtons = document.querySelectorAll('.customer-tab-button');
    const tabContents = document.querySelectorAll('.customer-tab-content');

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
        case 'tab-annual':
            createAnnualChart();
            break;
        case 'tab-monthly':
            createMonthlyChart();
            break;
        case 'tab-top-products':
            createProductsChart();
            break;
        case 'tab-top-categories':
            createCategoriesChart();
            break;
    }
}

function getChartIdForTab(tabId) {
    const chartIds = {
        'tab-annual-overview': 'annualSalesChart',
        'tab-top-products': 'topProductsChart',
        'tab-bottom-products': 'bottomProductsChart',
        'tab-category-analysis': 'categorySalesChart',
        'tab-annual': 'annualSalesChart',
        'tab-monthly': 'monthlySalesChart',
        'tab-top-products': 'topProductsChart',
        'tab-top-categories': 'topCategoriesChart'
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
                    'rgba(123, 82, 84, 0.8)',
                    'rgba(82, 84, 103, 0.8)',
                    'rgba(103, 84, 82, 0.8)',
                    'rgba(84, 82, 103, 0.8)',
                    'rgba(123, 84, 82, 0.8)'
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

// Customer Dashboard Charts
function createAnnualChart() {
    const ctx = document.getElementById('annualSalesChart')?.getContext('2d');
    if (!ctx) return;

    new Chart(ctx, {
        type: 'line',
        data: {
            labels: yearlyOrders.map(year => year),
            datasets: [{
                label: 'Annual Revenue',
                data: yearlyRevenue,
                borderColor: 'rgb(82, 103, 84)',
                backgroundColor: 'rgba(82, 103, 84, 0.1)',
                tension: 0.4,
                fill: true
            }]
        },
        options: getChartOptions('currency')
    });
}

function createMonthlyChart() {
    const ctx = document.getElementById('monthlySalesChart')?.getContext('2d');
    if (!ctx) return;

    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: monthlySalesLabels,
            datasets: [{
                label: 'Monthly Revenue',
                data: monthlySalesData,
                backgroundColor: 'rgba(82, 103, 84, 0.7)',
                borderColor: 'rgb(82, 103, 84)',
                borderWidth: 1
            }]
        },
        options: getChartOptions('currency')
    });
}

function createProductsChart() {
    const ctx = document.getElementById('topProductsChart')?.getContext('2d');
    if (!ctx) return;

    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: topProductsLabels,
            datasets: [{
                label: 'Products Sold',
                data: topProductsData,
                backgroundColor: 'rgba(82, 103, 84, 0.7)',
                borderColor: 'rgb(82, 103, 84)',
                borderWidth: 1
            }]
        },
        options: {
            ...getChartOptions('units'),
            indexAxis: 'y'
        }
    });
}

function createCategoriesChart() {
    const ctx = document.getElementById('topCategoriesChart')?.getContext('2d');
    if (!ctx) return;

    new Chart(ctx, {
        type: 'pie',
        data: {
            labels: topCategoriesLabels,
            datasets: [{
                data: topCategoriesData,
                backgroundColor: [
                    'rgba(82, 103, 84, 0.8)',
                    'rgba(103, 82, 84, 0.8)',
                    'rgba(84, 103, 82, 0.8)',
                    'rgba(123, 82, 84, 0.8)'
                ]
            }]
        },
        options: getChartOptions('units')
    });
}

function getChartOptions(type, title = '') {
    const baseOptions = {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
            legend: {
                position: 'bottom'
            },
            title: {
                display: !!title,
                text: title,
                padding: {
                    top: 10,
                    bottom: 10
                }
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
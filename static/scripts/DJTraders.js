console.log("DJTraders.js is loaded and running");

document.addEventListener('DOMContentLoaded', () => {
    console.log('Document ready in DJTraders.js');
    setupCustomerDashboardTabs();
    initializeChartForTab('tab-annual-overview');

    const filterForm = document.getElementById('customerFilterForm');
    console.log('Filter form found:', filterForm); // Debug log

    if (filterForm) {
        const clearButton = filterForm.querySelector('.btn-clear');
        const inputs = filterForm.querySelectorAll('input[type="text"], select');
        const countrySelect = document.getElementById('country');
        console.log('Country select found:', countrySelect); // Debug log

        if (clearButton) {
            clearButton.addEventListener('click', (e) => {
                e.preventDefault();
                console.log("Clear button clicked");  // Debug log
                inputs.forEach(input => {
                    if (input.type === 'text' || input.tagName === 'SELECT') {
                        input.value = '';
                    }
                });
                const letterInput = filterForm.querySelector('input[name="letter"]');
                if (letterInput) {
                    letterInput.remove();
                }
                filterForm.submit();
            });
        }

        if (countrySelect) {
            countrySelect.addEventListener('change', () => {
                console.log('Country changed to:', countrySelect.value); // Debug log
                filterForm.submit();
            });
        }
    } else {
        console.error('Customer filter form not found!');
    }
});

const chartInstances = {};

function setupCustomerDashboardTabs() {
    const tabButtons = document.querySelectorAll('.customer-tab-button');
    const tabContents = document.querySelectorAll('.customer-tab-content');

    tabButtons.forEach(button => {
        button.addEventListener('click', () => {
            tabButtons.forEach(btn => btn.classList.remove('active'));
            tabContents.forEach(content => content.classList.remove('active'));

            button.classList.add('active');
            const content = document.getElementById(button.dataset.tab);
            if (content) {
                content.classList.add('active');
                destroyChart(button.dataset.tab);
                initializeChartForTab(button.dataset.tab);
            }
        });
    });
}

function initializeChartForTab(tabId) {
    console.log(`Initializing chart for tab: ${tabId}`);
    let ctx;

    if (tabId === 'tab-annual-overview') {
        const chartElement = document.getElementById('annualSalesChart');
        if (chartElement) {
            ctx = chartElement.getContext('2d');
            chartInstances[tabId] = new Chart(ctx, {
                type: 'bar',
                data: {
                    labels: annualSalesLabels,
                    datasets: [{
                        label: 'Revenue',
                        data: annualSalesData,
                        backgroundColor: 'rgba(82, 103, 84, 0.6)',
                        borderColor: 'rgba(82, 103, 84, 1)',
                        borderWidth: 1
                    }]
                },
                options: {
                    responsive: true,
                    scales: { 
                        y: { 
                            beginAtZero: true,
                            ticks: {
                                callback: function(value) {
                                    return '$' + value.toLocaleString();
                                }
                            }
                        } 
                    }
                }
            });
        } else {
            console.warn("annualSalesChart element not found");
        }
    } else if (tabId === 'tab-top-products') {
        const chartElement = document.getElementById('topProductsChart');
        if (chartElement) {
            ctx = chartElement.getContext('2d');
            chartInstances[tabId] = new Chart(ctx, {
                type: 'bar',
                data: {
                    labels: topProductsLabels,
                    datasets: [{
                        label: 'Top Products Revenue',
                        data: topProductsData,
                        backgroundColor: 'rgba(103, 82, 84, 0.6)',
                        borderColor: 'rgba(103, 82, 84, 1)',
                        borderWidth: 1
                    }]
                },
                options: {
                    responsive: true,
                    scales: {
                        y: { 
                            beginAtZero: true,
                            ticks: {
                                callback: function(value) {
                                    return '$' + value.toLocaleString();
                                }
                            }
                        }
                    }
                }
            });
        } else {
            console.warn("topProductsChart element not found");
        }
    } else if (tabId === 'tab-bottom-products') {
        const chartElement = document.getElementById('bottomProductsChart');
        if (chartElement) {
            ctx = chartElement.getContext('2d');
            chartInstances[tabId] = new Chart(ctx, {
                type: 'bar',
                data: {
                    labels: bottomProductsLabels,
                    datasets: [{
                        label: 'Bottom Products Revenue',
                        data: bottomProductsData,
                        backgroundColor: 'rgba(84, 103, 82, 0.6)',
                        borderColor: 'rgba(84, 103, 82, 1)',
                        borderWidth: 1
                    }]
                },
                options: {
                    responsive: true,
                    scales: {
                        y: {
                            beginAtZero: true,
                            ticks: {
                                callback: function(value) {
                                    return '$' + value.toLocaleString();
                                }
                            }
                        }
                    }
                }
            });
        } else {
            console.warn("bottomProductsChart element not found");
        }
    } else if (tabId === 'tab-category-analysis') {
        const chartElement = document.getElementById('categorySalesChart');
        if (chartElement) {
            ctx = chartElement.getContext('2d');
            chartInstances[tabId] = new Chart(ctx, {
                type: 'pie',
                data: {
                    labels: categorySalesLabels,
                    datasets: [{
                        label: 'Category Sales',
                        data: categorySalesData,
                        backgroundColor: [
                            'rgba(82, 103, 84, 0.6)',
                            'rgba(103, 82, 84, 0.6)',
                            'rgba(84, 103, 82, 0.6)',
                            'rgba(123, 82, 84, 0.6)'
                        ],
                        borderColor: [
                            'rgba(82, 103, 84, 1)',
                            'rgba(103, 82, 84, 1)',
                            'rgba(84, 103, 82, 1)',
                            'rgba(123, 82, 84, 1)'
                        ],
                        borderWidth: 1
                    }]
                },
                options: {
                    responsive: true
                }
            });
        } else {
            console.warn("categorySalesChart element not found");
        }
    }
}

function destroyChart(tabId) {
    if (chartInstances[tabId]) {
        chartInstances[tabId].destroy();
        delete chartInstances[tabId];
    }
}

function archiveRecord(type, id) {
    const url = `/DjTraders/customers/${id}/archive/`;
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
            window.location.href = '/DjTraders/accounts/login/';
            return;
        }
        return response.json();
    })
    .then(data => {
        if (data && data.status === 'archived') window.location.reload();
    })
    .catch(error => console.error('Error:', error));
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

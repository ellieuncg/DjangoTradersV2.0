/* ==========================================================================
   Event Listener
========================================================================== */
document.addEventListener('DOMContentLoaded', function () {
    console.log('DOM Loaded');

    // Assume `salesDashboardData` is injected via the Django template
    if (typeof salesDashboardData !== "undefined") {
        initializeSalesDashboard(salesDashboardData);
    } else {
        console.error("Sales dashboard data not found.");
    }

    // Fetch customer dashboard data (if required)
    fetchCustomerDashboardData()
        .then(data => initializeCustomerDashboard(data))
        .catch(error => {
            console.error('Error fetching customer dashboard data:', error);
            handleCustomerDashboardError();
        });
});


function fetchCustomerDashboardData() {
    // Replace this with your actual data fetching logic
    return Promise.resolve({
        yearlyOrders: ['2021', '2022', '2023'],
        yearlyRevenue: [100000, 120000, 150000],
        monthlySalesLabels: ['Jan', 'Feb', 'Mar'],
        monthlySalesData: [30000, 40000, 35000],
        topProducts: {
            labels: ['Product A', 'Product B', 'Product C'],
            revenue: [50000, 40000, 35000]
        },
        topCategories: {
            labels: ['Category A', 'Category B', 'Category C'],
            revenue: [60000, 45000, 40000]
        }
    });
}

/* ==========================================================================
   CUSTOMER DASHBOARD
========================================================================== */

function initializeCustomerDashboard(customerDashboardData) {
    if (!customerDashboardData) {
        console.warn("Customer Dashboard data is missing.");
        return;
    }

    console.log("Initializing Customer Dashboard...");
    setupCustomerDashboardTabs(customerDashboardData);
}

function setupCustomerDashboardTabs(customerDashboardData) {
    console.log("Setting up Customer Dashboard tabs...");

    const tabButtons = document.querySelectorAll(".customer-tab-button");
    const tabContents = document.querySelectorAll(".customer-tab-content");

    if (!tabButtons.length || !tabContents.length) {
        console.warn("No tabs or content found for Customer Dashboard.");
        return;
    }

    // Add click event listeners to each tab button
    tabButtons.forEach((button) => {
        button.addEventListener("click", () => {
            // Reset all tabs and content
            tabButtons.forEach((btn) => btn.classList.remove("active"));
            tabContents.forEach((content) => content.classList.remove("active"));

            // Activate the clicked tab and its content
            button.classList.add("active");
            const targetTab = button.dataset.tab;
            const targetContent = document.getElementById(targetTab);
            if (targetContent) {
                targetContent.classList.add("active");
                console.log(`Activated tab: ${targetTab}`);
                handleCustomerDashboardCharts(targetTab, customerDashboardData);
            } else {
                console.warn(`No content found for tab: ${targetTab}`);
            }
        });
    });

    // Activate the first tab by default
    if (tabButtons.length > 0) {
        tabButtons[0].click();
    }
}

function handleCustomerDashboardCharts(tabId, customerDashboardData) {
    console.log(`Handling charts for tab: ${tabId}`);
    switch (tabId) {
        case "loyalty-tab":
            console.log("Loyalty Program Status tab clicked. No chart required.");
            break;
        case "annual-tab":
            createAnnualSalesChart(customerDashboardData);
            break;
        case "monthly-tab":
            createMonthlySalesChart(customerDashboardData);
            break;
        case "top-products-tab":
            createTopProductsYearChart(customerDashboardData);
            break;
        case "top-categories-tab":
            createTopCategoriesYearChart(customerDashboardData);
            break;
        default:
            console.warn(`No chart associated with tabId: ${tabId}`);
    }
}

/* ==========================================================================
   CHART CREATION FUNCTIONS
========================================================================== */

function createAnnualSalesChart(customerDashboardData) {
    const ctx = document.getElementById("annualSalesChart")?.getContext("2d");
    if (!ctx || !customerDashboardData.yearlyOrders || !customerDashboardData.yearlyRevenue) {
        console.warn("Required data for 'Annual Sales' chart is missing.");
        return;
    }

    new Chart(ctx, {
        type: "line",
        data: {
            labels: customerDashboardData.yearlyOrders,
            datasets: [{
                label: "Revenue",
                data: customerDashboardData.yearlyRevenue,
                borderColor: "rgba(82, 103, 84, 1)",
                backgroundColor: "rgba(82, 103, 84, 0.1)",
                fill: true
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { position: "top" },
                title: { display: true, text: "Annual Sales by Customer" }
            }
        }
    });
}

function createMonthlySalesChart(customerDashboardData) {
    const ctx = document.getElementById("monthlySalesChart")?.getContext("2d");
    if (!ctx || !customerDashboardData.monthlySalesLabels || !customerDashboardData.monthlySalesData) {
        console.warn("Required data for 'Monthly Sales' chart is missing.");
        return;
    }

    new Chart(ctx, {
        type: "bar",
        data: {
            labels: customerDashboardData.monthlySalesLabels,
            datasets: [{
                label: "Revenue",
                data: customerDashboardData.monthlySalesData,
                backgroundColor: "rgba(82, 103, 84, 0.7)"
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { position: "top" },
                title: { display: true, text: "Monthly Sales by Customer" }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    ticks: {
                        callback: (value) => `$${value.toLocaleString()}`
                    }
                }
            }
        }
    });
}

function createTopProductsYearChart(customerDashboardData) {
    const ctx = document.getElementById("topProductsChart")?.getContext("2d");
    if (!ctx || !customerDashboardData.topProducts?.labels || !customerDashboardData.topProducts?.revenue) {
        console.warn("Missing data for 'Top Products by Year' chart.");
        return;
    }

    new Chart(ctx, {
        type: "bar",
        data: {
            labels: customerDashboardData.topProducts.labels,
            datasets: [{
                label: "Revenue",
                data: customerDashboardData.topProducts.revenue,
                backgroundColor: "rgba(82, 103, 84, 0.7)"
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { position: "top" },
                title: { display: true, text: "Top Products by Year" }
            }
        }
    });
}

function createTopCategoriesYearChart(customerDashboardData) {
    const ctx = document.getElementById("topCategoriesChart")?.getContext("2d");
    if (!ctx || !customerDashboardData.topCategories?.labels || !customerDashboardData.topCategories?.revenue) {
        console.warn("Missing data for 'Top Categories by Year' chart.");
        return;
    }

    new Chart(ctx, {
        type: "pie",
        data: {
            labels: customerDashboardData.topCategories.labels,
            datasets: [{
                data: customerDashboardData.topCategories.revenue,
                backgroundColor: [
                    "rgba(82, 103, 84, 0.8)",
                    "rgba(103, 82, 84, 0.8)",
                    "rgba(84, 103, 82, 0.8)",
                    "rgba(123, 82, 84, 0.8)"
                ]
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { position: "right" },
                title: { display: true, text: "Top Categories by Year" }
            }
        }
    });
}

/* ==========================================================================
   SALES DASHBOARD
========================================================================== */
function initializeSalesDashboard(data) {
    console.log("Initializing Sales Dashboard", data);

    const tabButtons = document.querySelectorAll(".sales-tab-button");
    const tabContents = document.querySelectorAll(".sales-tab-content");

    tabButtons.forEach((button, index) => {
        button.addEventListener("click", () => {
            // Toggle Active Tab
            tabButtons.forEach((btn) => btn.classList.remove("active"));
            button.classList.add("active");

            // Toggle Active Content
            tabContents.forEach((content) => content.classList.remove("active"));
            tabContents[index].classList.add("active");

            // Render Charts
            if (index === 0) createChart("line", "annualSalesChart", data.annualSalesLabels, data.annualSalesData, "Annual Sales Overview");
            else if (index === 1) createChart("bar", "monthlySalesChart", data.monthlySalesLabels, data.monthlySalesData, "Monthly Sales Analysis");
            else if (index === 2) createChart("bar", "topProductsChart", data.topProductsLabels, data.topProductsData, "Top 10 Products");
            else if (index === 3) createChart("bar", "bottomProductsChart", data.bottomProductsLabels, data.bottomProductsData, "Bottom 10 Products");
            else if (index === 4) createChart("pie", "categorySalesChart", data.categorySalesLabels, data.categorySalesData, "Category Sales Analysis");
        });
    });

    // Initialize First Chart
    createChart("line", "annualSalesChart", data.annualSalesLabels, data.annualSalesData, "Annual Sales Overview");
}


// Initialize the Sales Dashboard on DOM load
document.addEventListener('DOMContentLoaded', function () {
    if (window.salesDashboardData) {
        initializeSalesDashboard(window.salesDashboardData);
    } else {
        console.error("Sales dashboard data not found.");
    }
});


function setupSalesDashboardTabs() {
    const salesTabButtons = document.querySelectorAll(".sales-tab-button");
    const salesTabContents = document.querySelectorAll(".sales-tab-content");

    if (salesTabButtons.length && salesTabContents.length) {
        console.log("Setting up Sales Dashboard Tabs...");
        salesTabButtons.forEach((button) => {
            button.addEventListener("click", () => {
                // Reset active states
                salesTabButtons.forEach((btn) => btn.classList.remove("active"));
                salesTabContents.forEach((content) => content.classList.remove("active"));

                // Activate selected tab and content
                button.classList.add("active");
                const targetTab = button.dataset.tab;
                const targetContent = document.getElementById(targetTab);
                if (targetContent) {
                    targetContent.classList.add("active");
                    initializeChartForTab(targetTab);
                } else {
                    console.warn(`No content found for tab: ${targetTab}`);
                }
            });
        });
    } else {
        console.warn("No Sales Dashboard tabs or content found.");
    }
}


/* ==========================================================================
   MONTHLY SALES CHART
========================================================================== */


/* ==========================================================================
   TOP PRODUCTS BY YEAR CHART
========================================================================== */
function createTopProductsYearChart() {
    const ctx = document.getElementById("topProductsYearChart")?.getContext("2d");
    if (!ctx) {
        console.warn("Canvas for 'Top Products by Year' chart not found.");
        return;
    }

    if (!customerDashboardData.topProducts?.labels || !customerDashboardData.topProducts?.revenue) {
        console.warn("Missing data for 'Top Products by Year' chart.");
        return;
    }

    new Chart(ctx, {
        type: "bar",
        data: {
            labels: customerDashboardData.topProducts.labels,
            datasets: [{
                label: "Revenue",
                data: customerDashboardData.topProducts.revenue,
                backgroundColor: "rgba(82, 103, 84, 0.7)"
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { position: 'top' },
                title: {
                    display: true,
                    text: "Top Products by Year"
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    ticks: {
                        callback: function(value) {
                            return `$${value.toLocaleString()}`;
                        }
                    }
                }
            }
        }
    });
}

/* ==========================================================================
   TOP CATEGORIES BY YEAR CHART
========================================================================== */
function createTopCategoriesYearChart() {
    const ctx = document.getElementById("topCategoriesYearChart")?.getContext("2d");
    if (!ctx) {
        console.warn("Canvas for 'Top Categories by Year' chart not found.");
        return;
    }

    if (!customerDashboardData.topCategories?.labels || !customerDashboardData.topCategories?.revenue) {
        console.warn("Missing data for 'Top Categories by Year' chart.");
        return;
    }

    new Chart(ctx, {
        type: "pie",
        data: {
            labels: customerDashboardData.topCategories.labels,
            datasets: [{
                data: customerDashboardData.topCategories.revenue,
                backgroundColor: [
                    "rgba(82, 103, 84, 0.8)",
                    "rgba(103, 82, 84, 0.8)",
                    "rgba(84, 103, 82, 0.8)",
                    "rgba(123, 82, 84, 0.8)"
                ]
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { position: 'right' },
                title: {
                    display: true,
                    text: "Top Categories by Year"
                }
            }
        }
    });
}

/* ==========================================================================
   SCOPE DASHBOARDS
========================================================================== */

const CUSTOMER_TABS = {
    LOYALTY: "loyalty-tab",
    ANNUAL: "annual-tab",
    MONTHLY: "monthly-tab",
    TOP_PRODUCTS: "top-products-tab",
    TOP_CATEGORIES: "top-categories-tab"
};

const SALES_TABS = {
    ANNUAL: "tab-annual-overview",
    MONTHLY: "tab-monthly-analysis",
    TOP_PRODUCTS: "tab-top-products",
    CATEGORY: "tab-category-analysis"
};



/* ==========================================================================
   EVENT LISTENER TWO
========================================================================== */

/* document.addEventListener('DOMContentLoaded', function () {
    setupSalesDashboardTabs();

    // Check which dashboard is active and initialize the first tab
    if (document.querySelector('.sales-tab-button')) {
        console.log('Initializing Sales Dashboard...');
        initializeChartForTab(TABS.SALES.ANNUAL); // Use TABS object for consistency
    } else if (document.querySelector('.customer-tab-button')) {
        console.log('Initializing Customer Dashboard...');
        const firstCustomerTab = document.querySelector('.customer-tab-button');
        if (firstCustomerTab) {
            firstCustomerTab.click(); // Automatically activate the first tab
        } else {
            console.warn('No customer tab buttons found.');
        }
    } else {
        console.warn('No dashboard tabs detected.');
    }
});
 */
/* ==========================================================================
   SALES DASHBOARD TABS
========================================================================== */

function setupSalesDashboardTabs() {
    const salesTabButtons = document.querySelectorAll(".sales-tab-button");
    const salesTabContents = document.querySelectorAll(".sales-tab-content");

    if (salesTabButtons.length && salesTabContents.length) {
        console.log("Setting up Sales Dashboard Tabs...");
        
        // Attach click event listeners to each tab button
        salesTabButtons.forEach((button) => {
            button.addEventListener("click", () => {
                // Reset active classes
                salesTabButtons.forEach((btn) => btn.classList.remove("active"));
                salesTabContents.forEach((content) => content.classList.remove("active"));

                // Activate clicked tab and its corresponding content
                button.classList.add("active");
                const targetTab = button.dataset.tab;
                const targetContent = document.getElementById(targetTab);

                if (targetContent) {
                    targetContent.classList.add("active");
                    console.log(`Activated tab: ${targetTab}`);
                    initializeChartForTab(targetTab); // Render chart for the active tab
                } else {
                    console.warn(`No content found for tab: ${targetTab}`);
                }
            });
        });

        // Activate the first tab by default
        console.log("Activating the first tab by default...");
        salesTabButtons[0]?.click();
    } else {
        console.warn("No Sales Dashboard tabs or content found.");
    }
}


/* ==========================================================================
   SALES CHART CREATION
========================================================================== */

// Shared chart configuration to avoid repetition
const CHART_OPTIONS = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
        legend: { position: 'top' },
        title: { display: true }
    }
};

// Create the "Annual Overview" chart
/* function createAnnualOverviewChart() {
    const ctx = document.getElementById("annualSalesChart")?.getContext("2d");
    if (!ctx) {
        console.warn("Canvas for 'Annual Overview' chart not found.");
        return;
    }

    if (!salesDashboardData || !salesDashboardData.annualLabels || !salesDashboardData.annualData) {
        console.warn("Required data for 'Annual Overview' chart is missing.");
        return;
    }

    new Chart(ctx, {
        type: "line",
        data: {
            labels: salesDashboardData.annualLabels,
            datasets: [
                {
                    label: "Revenue",
                    data: salesDashboardData.annualData,
                    borderColor: "rgba(82, 103, 84, 1)",
                    backgroundColor: "rgba(82, 103, 84, 0.1)",
                    fill: true,
                },
            ],
        },
        options: {
            ...CHART_OPTIONS,
            plugins: {
                ...CHART_OPTIONS.plugins,
                title: {
                    ...CHART_OPTIONS.plugins.title,
                    text: "Annual Sales Overview"
                }
            }
        }
    });
} */

// Create the "Monthly Analysis" chart
function createMonthlyAnalysisChart() {
    const ctx = document.getElementById("monthlySalesChart")?.getContext("2d");
    if (!ctx) {
        console.warn("Canvas for 'Monthly Analysis' chart not found.");
        return;
    }

    if (!salesDashboardData || !salesDashboardData.monthlyLabels || !salesDashboardData.monthlyData) {
        console.warn("Required data for 'Monthly Analysis' chart is missing.");
        return;
    }

    new Chart(ctx, {
        type: "bar",
        data: {
            labels: salesDashboardData.monthlyLabels,
            datasets: [
                {
                    label: "Revenue",
                    data: salesDashboardData.monthlyData,
                    backgroundColor: "rgba(82, 103, 84, 0.7)",
                    borderColor: "rgba(82, 103, 84, 1)",
                    borderWidth: 1,
                },
            ],
        },
        options: {
            ...CHART_OPTIONS,
            plugins: {
                ...CHART_OPTIONS.plugins,
                title: {
                    ...CHART_OPTIONS.plugins.title,
                    text: "Monthly Sales Analysis"
                }
            }
        }
    });
}

// Create the "Top Products" chart
function createTopProductsChart() {
    const ctx = document.getElementById("topProductsChart")?.getContext("2d");
    if (!ctx) {
        console.warn("Canvas for 'Top Products' chart not found.");
        return;
    }

    if (!salesDashboardData || !salesDashboardData.topProductsLabels || !salesDashboardData.topProductsData) {
        console.warn("Required data for 'Top Products' chart is missing.");
        return;
    }

    new Chart(ctx, {
        type: "bar",
        data: {
            labels: salesDashboardData.topProductsLabels,
            datasets: [
                {
                    label: "Revenue",
                    data: salesDashboardData.topProductsData,
                    backgroundColor: "rgba(103, 82, 84, 0.7)",
                    borderColor: "rgba(103, 82, 84, 1)",
                    borderWidth: 1,
                },
            ],
        },
        options: {
            ...CHART_OPTIONS,
            plugins: {
                ...CHART_OPTIONS.plugins,
                title: {
                    ...CHART_OPTIONS.plugins.title,
                    text: "Top 10 Products by Revenue"
                }
            }
        }
    });
}

// Create the "Bottom Products" chart
/* function createBottomProductsChart() {
    const ctx = document.getElementById("bottomProductsChart")?.getContext("2d");
    if (!ctx) {
        console.warn("Canvas for 'Bottom Products' chart not found.");
        return;
    }

    if (!salesDashboardData || !salesDashboardData.bottomProductsLabels || !salesDashboardData.bottomProductsData) {
        console.warn("Required data for 'Bottom Products' chart is missing.");
        return;
    }

    new Chart(ctx, {
        type: "bar",
        data: {
            labels: salesDashboardData.bottomProductsLabels,
            datasets: [
                {
                    label: "Revenue",
                    data: salesDashboardData.bottomProductsData,
                    backgroundColor: "rgba(82, 103, 84, 0.7)",
                    borderColor: "rgba(82, 103, 84, 1)",
                    borderWidth: 1,
                },
            ],
        },
        options: {
            ...CHART_OPTIONS,
            plugins: {
                ...CHART_OPTIONS.plugins,
                title: {
                    ...CHART_OPTIONS.plugins.title,
                    text: "Bottom 10 Products by Revenue"
                }
            }
        }
    });
} */

// Create the "Category Sales" chart
function createCategorySalesChart() {
    const ctx = document.getElementById("categorySalesChart")?.getContext("2d");
    if (!ctx) {
        console.warn("Canvas for 'Category Sales' chart not found.");
        return;
    }

    if (!salesDashboardData || !salesDashboardData.categorySalesLabels || !salesDashboardData.categorySalesData) {
        console.warn("Required data for 'Category Sales' chart is missing.");
        return;
    }

    new Chart(ctx, {
        type: "pie",
        data: {
            labels: salesDashboardData.categorySalesLabels,
            datasets: [
                {
                    label: "Revenue",
                    data: salesDashboardData.categorySalesData,
                    backgroundColor: [
                        "rgba(82, 103, 84, 0.8)",
                        "rgba(103, 82, 84, 0.8)",
                        "rgba(84, 103, 82, 0.8)",
                        "rgba(123, 82, 84, 0.8)",
                    ],
                },
            ],
        },
        options: {
            ...CHART_OPTIONS,
            plugins: {
                ...CHART_OPTIONS.plugins,
                title: {
                    ...CHART_OPTIONS.plugins.title,
                    text: "Category Sales Analysis"
                },
                legend: { position: "right" }
            }
        }
    });
}



/* ==========================================================================
   initializeChartForTab
========================================================================== */
function initializeChartForTab(tabId) {
    console.log(`Initializing chart for tab: ${tabId}`);

    const isSalesTab = Object.values(TABS.SALES).includes(tabId);
    const isCustomerTab = Object.values(TABS.CUSTOMER).includes(tabId);

    if (isSalesTab) {
        initializeSalesChart(tabId);
    } else if (isCustomerTab) {
        initializeCustomerChart(tabId);
    } else {
        console.warn(`No chart found for tab: ${tabId}`);
    }
}


// Helper function: Initialize Sales Dashboard charts
function initializeSalesChart(tabId) {
    // Destroy only sales-related charts
    ["annualSalesChart", "monthlySalesChart", "topProductsChart", "bottomProductsChart", "categorySalesChart"].forEach((chartId) => {
        const existingChart = Chart.getChart(chartId);
        if (existingChart) {
            existingChart.destroy();
        }
    });

    // Switch case for initializing sales charts
switch (tabId) {
    case TABS.SALES.ANNUAL:
        createAnnualOverviewChart(); // Initialize the Annual Sales Overview chart
        break;
    case TABS.SALES.MONTHLY:
        createMonthlyAnalysisChart(); // Initialize the Monthly Sales Analysis chart
        break;
    case TABS.SALES.TOP_PRODUCTS:
        createTopProductsChart(); // Initialize the Top Products by Revenue chart
        break;
    case TABS.SALES.BOTTOM_PRODUCTS:
        createBottomProductsChart(); // Initialize the Bottom Products by Revenue chart
        break;
    case TABS.SALES.CATEGORY:
        createCategorySalesChart(); // Initialize the Category Sales Analysis chart
        break;
    default:
        console.warn('No matching sales chart for tabId:', tabId); // Log a warning if no match
}

// Helper function: Initialize Customer Dashboard charts
function initializeCustomerChart(tabId) {
    // Destroy only customer-related charts
    ["topProductsYearChart", "topCategoriesYearChart"].forEach((chartId) => {
        const existingChart = Chart.getChart(chartId);
        if (existingChart) {
            existingChart.destroy();
        }
    });

    // Switch case for initializing customer charts
    switch (tabId) {
        case TABS.CUSTOMER.TOP_PRODUCTS:
            createTopProductsYearChart();
            break;
        case TABS.CUSTOMER.TOP_CATEGORIES:
            createTopCategoriesYearChart();
            break;
        default:
            console.warn('No matching customer chart for tabId:', tabId);
    }
}

/* ==========================================================================
   createBottomProductsChart
========================================================================== */
function createBottomProductsChart() {
    const ctx = document.getElementById("bottomProductsChart")?.getContext("2d");
    if (!ctx) return;

    new Chart(ctx, {
        type: "bar",
        data: {
            labels: salesDashboardData.bottomProductsLabels,
            datasets: [
                {
                    label: "Revenue",
                    data: salesDashboardData.bottomProductsData,
                    backgroundColor: "rgba(82, 103, 84, 0.7)",
                    borderColor: "rgba(82, 103, 84, 1)",
                    borderWidth: 1,
                },
            ],
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                title: {
                    display: true,
                    text: "Bottom 10 Products by Revenue",
                },
            },
        },
    });
}

/* ==========================================================================
   createCategorySalesChart
========================================================================== */
function createCategorySalesChart() {
    const ctx = document.getElementById("categorySalesChart")?.getContext("2d");
    if (!ctx) {
        console.warn("Canvas for 'Category Sales' chart not found.");
        return;
    }

    if (!salesDashboardData || !salesDashboardData.categorySalesLabels || !salesDashboardData.categorySalesData) {
        console.warn("Required data for 'Category Sales' chart is missing or incomplete.");
        return;
    }

    const colors = [
        "rgba(82, 103, 84, 0.8)",
        "rgba(103, 82, 84, 0.8)",
        "rgba(84, 103, 82, 0.8)",
        "rgba(123, 82, 84, 0.8)",
    ];

    // Dynamically assign colors if there are more categories than predefined colors
    const backgroundColors = salesDashboardData.categorySalesLabels.map(
        (_, index) => colors[index % colors.length]
    );

    new Chart(ctx, {
        type: "pie",
        data: {
            labels: salesDashboardData.categorySalesLabels,
            datasets: [
                {
                    label: "Revenue",
                    data: salesDashboardData.categorySalesData,
                    backgroundColor: backgroundColors,
                },
            ],
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    position: "right",
                },
                title: {
                    display: true,
                    text: "Category Sales Analysis",
                },
            },
        },
    });

    console.info("'Category Sales' chart created successfully.");
}


/* ==========================================================================
   Order Table Calculations
========================================================================== */
function calculateOrderTableTotals() {
    const table = document.querySelector('.product-detail__table');
    if (!table) {
        console.warn('Product detail table not found.');
        return;
    }

    const rows = table.querySelectorAll('tbody tr');
    let total = 0;

    rows.forEach(row => {
        const amountCell = row.querySelector('td:last-child');
        if (amountCell) {
            const amountText = amountCell.textContent;
            const amount = parseFloat(amountText.replace(/[$,]/g, '')) || 0;
            total += amount;
        }
    });

    const totalCell = table.querySelector('tfoot td:last-child');
    if (totalCell) {
        totalCell.innerHTML = `<strong>$${total.toFixed(2)}</strong>`;
    } else {
        console.warn('Footer cell for total not found.');
    }

    console.info(`Total calculated: $${total.toFixed(2)}`);
}

/* ==========================================================================
   Product Detail Page Sorting
========================================================================== */
function setupProductDetailSorting() {
    const sortSelect = document.getElementById("orderSort");
    if (!sortSelect) {
        console.warn("Sort dropdown (#orderSort) not found.");
        return;
    }

    sortSelect.addEventListener("change", (e) => {
        const tbody = document.querySelector('.product-detail__table tbody');
        if (!tbody) {
            console.warn("Table body for product details not found.");
            return;
        }

        const rows = Array.from(tbody.getElementsByTagName('tr'));
        if (rows.length <= 1) {
            console.info("Not enough rows to sort.");
            return;
        }

        const sortType = e.target.value; // E.g., "date-asc", "quantity", "total"
        const columnIndex = getColumnIndex(sortType);
        if (columnIndex === -1) {
            console.warn("Invalid sort type selected:", sortType);
            return;
        }

        // Sort rows based on selected criteria
        rows.sort((a, b) => {
            const aVal = a.cells[columnIndex]?.textContent.trim() || "";
            const bVal = b.cells[columnIndex]?.textContent.trim() || "";

            if (sortType.includes('date')) {
                return compareDates(aVal, bVal, sortType === 'date-asc');
            } else if (sortType === 'quantity') {
                return compareNumbers(aVal, bVal);
            } else if (sortType === 'total') {
                return comparePrice(aVal, bVal);
            }
            return 0;
        });

        // Re-append sorted rows to the table
        rows.forEach((row) => tbody.appendChild(row));

        // Update totals after sorting
        calculateOrderTableTotals();

        console.info(`Table sorted by: ${sortType}`);
    });
}

/**
 * Map sort type to corresponding column index.
 * @param {string} sortType - Type of sorting (e.g., "date-asc").
 * @returns {number} Column index or -1 if invalid.
 */
function getColumnIndex(sortType) {
    switch (sortType) {
        case 'date-desc':
        case 'date-asc':
            return 1; // Date column
        case 'quantity':
            return 2; // Quantity column
        case 'total':
            return 3; // Total column
        default:
            return -1; // Invalid sort type
    }
}

/**
 * Compare two dates for sorting.
 * @param {string} a - First date value.
 * @param {string} b - Second date value.
 * @param {boolean} asc - Whether to sort in ascending order.
 * @returns {number} Comparison result.
 */
function compareDates(a, b, asc) {
    const dateA = new Date(a);
    const dateB = new Date(b);
    return asc ? dateA - dateB : dateB - dateA;
}

/**
 * Compare two numbers for sorting.
 * @param {string} a - First numeric value.
 * @param {string} b - Second numeric value.
 * @returns {number} Comparison result.
 */
function compareNumbers(a, b) {
    const numA = parseInt(a, 10) || 0;
    const numB = parseInt(b, 10) || 0;
    return numA - numB;
}

/**
 * Compare two monetary values for sorting.
 * @param {string} a - First price value (e.g., "$100.00").
 * @param {string} b - Second price value (e.g., "$50.00").
 * @returns {number} Comparison result.
 */
function comparePrice(a, b) {
    const priceA = parseFloat(a.replace(/[$,]/g, '')) || 0;
    const priceB = parseFloat(b.replace(/[$,]/g, '')) || 0;
    return priceA - priceB;
}

/* ==========================================================================
   COUPLE SHORT FUNCTIONS
========================================================================== */

/**
 * Get the column index based on the sort type.
 * @param {string} sortType - Type of sorting (e.g., "date-asc").
 * @returns {number} Column index or -1 if invalid.
 */
function getColumnIndex(sortType) {
    switch (sortType) {
        case 'date-desc':
        case 'date-asc':
            return 1; // Date column
        case 'quantity':
            return 2; // Quantity column
        case 'total':
            return 3; // Total column
        default:
            console.warn(`Invalid sortType: ${sortType}`);
            return -1; // Invalid column index
    }
}

/**
 * Compare two dates for sorting.
 * @param {string} a - First date value.
 * @param {string} b - Second date value.
 * @param {boolean} asc - Whether to sort in ascending order.
 * @returns {number} Comparison result.
 */
function compareDates(a, b, asc = true) {
    const dateA = new Date(a);
    const dateB = new Date(b);

    if (isNaN(dateA) || isNaN(dateB)) {
        console.warn(`Invalid date(s) for comparison: ${a}, ${b}`);
        return 0;
    }

    return asc ? dateA - dateB : dateB - dateA;
}

/**
 * Compare two numbers for sorting.
 * @param {string|number} a - First numeric value.
 * @param {string|number} b - Second numeric value.
 * @returns {number} Comparison result.
 */
function compareNumbers(a, b) {
    const numA = parseInt(a, 10) || 0;
    const numB = parseInt(b, 10) || 0;
    return numA - numB;
}

/**
 * Compare two monetary values for sorting.
 * @param {string} a - First price value (e.g., "$100.00").
 * @param {string} b - Second price value (e.g., "$50.00").
 * @returns {number} Comparison result.
 */
function comparePrice(a, b) {
    const priceA = parseFloat(a.replace(/[$,]/g, '')) || 0;
    const priceB = parseFloat(b.replace(/[$,]/g, '')) || 0;
    return priceA - priceB;
}

/* ==========================================================================
   Archive Record Functionality
========================================================================== */
function archiveRecord(recordType, recordId) {
    console.log('archiveRecord function called with:', { recordType, recordId });

    const csrfTokenElement = document.querySelector('[name=csrfmiddlewaretoken]');
    if (!csrfTokenElement) {
        console.error('CSRF token not found.');
        alert('An error occurred. Please refresh the page and try again.');
        return;
    }
    const csrfToken = csrfTokenElement.value;

    let url;
    switch (recordType) {
        case 'customer':
            url = `${window.location.pathname}${recordId}/archive/`;
            break;
        // Add more cases here for other record types, if needed
        default:
            console.error('Unsupported record type:', recordType);
            alert('Unsupported record type.');
            return;
    }

    console.log('Attempting to archive. Full URL:', window.location.origin + url);

    if (!confirm('Are you sure you want to archive this record?')) {
        console.log('Archive cancelled by user');
        return;
    }

    fetch(url, {
        method: 'POST',
        headers: {
            'X-CSRFToken': csrfToken,
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        },
        credentials: 'same-origin'
    })
    .then(response => {
        console.log('Response received:', response.status);
        if (!response.ok) {
            return response.json().then(data => {
                const errorMessage = data.message || 'An error occurred while archiving the record.';
                console.error('Error response:', data);
                throw new Error(errorMessage);
            });
        }
        return response.json();
    })
    .then(data => {
        console.log('Success response:', data);
        if (data.status === 'archived') {
            updateUIAfterArchiving(recordType, recordId, data.message);
        } else {
            alert('Failed to archive record: ' + (data.message || 'Unknown error'));
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Failed to archive record: ' + error.message);
    });
}

function updateUIAfterArchiving(recordType, recordId, message) {
    let recordElement;

    switch (recordType) {
        case 'customer':
            recordElement = document.querySelector(`[data-customer-id="${recordId}"]`);
            break;
        // Add cases for other record types if needed
        default:
            console.error('Unsupported record type for UI update:', recordType);
            return;
    }

    if (recordElement) {
        recordElement.classList.remove('active', 'inactive');
        recordElement.classList.add('archived');

        const statusElement = recordElement.querySelector('.status');
        if (statusElement) {
            statusElement.innerHTML = '<strong>Status:</strong> Archived';
        }

        const archiveButton = recordElement.querySelector('.btn-archive');
        if (archiveButton) {
            archiveButton.disabled = true;
            archiveButton.setAttribute('aria-disabled', 'true');
        }

        if (message) {
            alert(message);
        }

        const statusFilter = document.getElementById('statusFilter');
        if (statusFilter && statusFilter.value === 'active') {
            location.reload();
        }
    } else {
        console.warn('Record element not found in DOM for recordId:', recordId);
    }
}

/* ==========================================================================
   DOM THREE: Filter Form Handling
========================================================================== */

document.addEventListener('DOMContentLoaded', function() {
    const filterForm = document.getElementById('filterForm');
    if (!filterForm) {
        console.warn('Filter form not found.');
        return;
    }

    filterForm.addEventListener('submit', function(e) {
        e.preventDefault();

        const yearInput = document.getElementById('year');
        const productInput = document.getElementById('product');

        if (!yearInput || !productInput) {
            console.error('Year or product input element is missing.');
            alert('Unable to apply filters. Please try again later.');
            return;
        }

        const year = yearInput.value.trim();
        const product = productInput.value.trim();
        const queryParams = new URLSearchParams();

        // Validate and append year and product filters
        if (year) {
            if (isNaN(year) || year.length !== 4) {
                alert('Please enter a valid year (e.g., 2024).');
                return;
            }
            queryParams.set('year', year);
        }

        if (product) {
            if (product.length > 50) {
                alert('Product name is too long. Please shorten it.');
                return;
            }
            queryParams.set('product', product);
        }

        // If no filters are provided, reload the page without filters
        if (!queryParams.toString()) {
            if (!confirm('No filters applied. Reload the page with all data?')) {
                return;
            }
        }

        // Update URL and reload the page
        const newUrl = `${window.location.pathname}?${queryParams.toString()}`;
        console.log('Redirecting to:', newUrl);
        window.location.href = newUrl;
    });
});

/* ==========================================================================
   createTopProductsChart
========================================================================== */
function createTopProductsChart() {
    const ctx = document.getElementById("topProductsChart")?.getContext("2d");
    if (!ctx) {
        console.warn("Canvas for 'Top Products' chart not found.");
        return;
    }

    if (!salesDashboardData || !salesDashboardData.topProductsLabels || !salesDashboardData.topProductsData) {
        console.warn("Required data for 'Top Products' chart is missing.");
        return;
    }

    const backgroundColors = salesDashboardData.topProductsData.map(() => "rgba(103, 82, 84, 0.7)");
    const borderColors = salesDashboardData.topProductsData.map(() => "rgba(103, 82, 84, 1)");

    new Chart(ctx, {
        type: "bar",
        data: {
            labels: salesDashboardData.topProductsLabels,
            datasets: [
                {
                    label: "Revenue",
                    data: salesDashboardData.topProductsData,
                    backgroundColor: backgroundColors,
                    borderColor: borderColors,
                    borderWidth: 1,
                },
            ],
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'top'
                },
                title: {
                    display: true,
                    text: "Top 10 Products by Revenue"
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    ticks: {
                        callback: function(value) {
                            return `$${value.toLocaleString()}`;
                        }
                    }
                }
            }
        }
    });
}

/* ==========================================================================
   CUSTOMER DASHBOARD CHARTS
========================================================================== */
function handleCustomerDashboardCharts(tabId, customerDashboardData) {
    switch (tabId) {
        case "annual-tab":
            createAnnualSalesChart(customerDashboardData);
            break;
        case "monthly-tab":
            createMonthlySalesChart(customerDashboardData);
            break;
        case "top-products-tab": // Match "Top Products by Year"
            createTopProductsYearChart(customerDashboardData);
            break;
        case "top-categories-tab": // Match "Top Categories by Year"
            createTopCategoriesYearChart(customerDashboardData);
            break;
        default:
            console.warn("No chart associated with tabId:", tabId);
    }
    
}

function createAnnualSalesChart(customerDashboardData) {
    const ctx = document.getElementById("annualSalesChart")?.getContext("2d");
    if (!ctx || !customerDashboardData.yearlyOrders || !customerDashboardData.yearlyRevenue) {
        console.warn("Required data for 'Annual Sales' chart is missing.");
        return;
    }

    new Chart(ctx, {
        type: "line",
        data: {
            labels: customerDashboardData.yearlyOrders,
            datasets: [{
                label: "Revenue",
                data: customerDashboardData.yearlyRevenue,
                borderColor: "rgba(82, 103, 84, 1)",
                backgroundColor: "rgba(82, 103, 84, 0.1)",
                fill: true
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { position: 'top' },
                title: {
                    display: true,
                    text: "Annual Sales by Customer"
                }
            }
        }
    });
}

function createMonthlySalesChart(customerDashboardData) {
    const ctx = document.getElementById("monthlySalesChart")?.getContext("2d");
    if (!ctx || !customerDashboardData.monthlySalesLabels || !customerDashboardData.monthlySalesData) {
        console.warn("Required data for 'Monthly Sales' chart is missing.");
        return;
    }

    new Chart(ctx, {
        type: "bar",
        data: {
            labels: customerDashboardData.monthlySalesLabels,
            datasets: [{
                label: "Revenue",
                data: customerDashboardData.monthlySalesData,
                backgroundColor: "rgba(82, 103, 84, 0.7)"
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { position: "top" },
                title: {
                    display: true,
                    text: "Monthly Sales by Customer"
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    ticks: {
                        callback: function(value) {
                            return `$${value.toLocaleString()}`;
                        }
                    }
                }
            }
        }
    });
}



/* ==========================================================================
   CUSTOMER CHART
========================================================================== */
function initializeCustomerChart(tabId) {
    console.log('Initializing customer chart for:', tabId);

    if (!customerDashboardData) {
        console.warn("Customer Dashboard data is missing.");
        return;
    }

    switch (tabId) {
        case 'top-products-year-tab': {
            const productsCtx = document.getElementById("topProductsYearChart")?.getContext("2d");
            if (!productsCtx) {
                console.warn("Canvas for 'Top Products by Year' chart not found.");
                return;
            }
            if (!customerDashboardData.topProducts?.labels || !customerDashboardData.topProducts?.revenue) {
                console.warn("Missing data for 'Top Products by Year' chart.");
                return;
            }
            new Chart(productsCtx, {
                type: "bar",
                data: {
                    labels: customerDashboardData.topProducts.labels,
                    datasets: [{
                        label: "Revenue",
                        data: customerDashboardData.topProducts.revenue,
                        backgroundColor: "rgba(82, 103, 84, 0.7)"
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: { position: 'top' },
                        title: {
                            display: true,
                            text: "Top Products by Year"
                        }
                    },
                    scales: {
                        y: {
                            beginAtZero: true,
                            ticks: {
                                callback: function(value) {
                                    return `$${value.toLocaleString()}`;
                                }
                            }
                        }
                    }
                }
            }); // Correct closing of the Chart object here
            break; // This break is now correctly placed outside the object
        }

        case 'top-categories-year-tab': {
            const categoriesCtx = document.getElementById("topCategoriesYearChart")?.getContext("2d");
            if (!categoriesCtx) {
                console.warn("Canvas for 'Top Categories by Year' chart not found.");
                return;
            }
            if (!customerDashboardData.topCategories?.labels || !customerDashboardData.topCategories?.revenue) {
                console.warn("Missing data for 'Top Categories by Year' chart.");
                return;
            }
            new Chart(categoriesCtx, {
                type: "pie",
                data: {
                    labels: customerDashboardData.topCategories.labels,
                    datasets: [{
                        data: customerDashboardData.topCategories.revenue,
                        backgroundColor: [
                            "rgba(82, 103, 84, 0.8)",
                            "rgba(103, 82, 84, 0.8)",
                            "rgba(84, 103, 82, 0.8)",
                            "rgba(123, 82, 84, 0.8)"
                        ]
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: { position: 'right' },
                        title: {
                            display: true,
                            text: "Top Categories by Year"
                        }
                    }
                }
            });
            break; // Correctly placed break statement
        }

        default:
            console.warn("No chart associated with tabId:", tabId);
    }
}

/* ==========================================================================
   CUSTOMER DASHBOARD TABS
========================================================================== */
function setupCustomerDashboardTabs() {
    console.log("Initializing Customer Dashboard Tabs...");
    
    const tabButtons = document.querySelectorAll(".customer-tab-button");
    const tabContents = document.querySelectorAll(".customer-tab-content");

    if (!tabButtons.length || !tabContents.length) {
        console.warn("No tabs or content found for Customer Dashboard.");
        return;
    }

    // Add click event listeners to tab buttons
    tabButtons.forEach((button) => {
        button.addEventListener("click", () => {
            console.log(`Tab clicked: ${button.dataset.tab}`);

            // Reset all tabs and content
            tabButtons.forEach((btn) => btn.classList.remove("active"));
            tabContents.forEach((content) => content.classList.remove("active"));

            // Activate clicked tab and corresponding content
            button.classList.add("active");
            const targetTab = button.dataset.tab;
            const targetContent = document.getElementById(targetTab);
            if (targetContent) {
                targetContent.classList.add("active");
                console.log(`Activated tab content: #${targetTab}`);
            } else {
                console.warn(`No content found for tab: ${targetTab}`);
            }
        });
    });

    // Activate the first tab by default
    if (tabButtons.length > 0) {
        tabButtons[0].click();
    }
}

// Initialize tabs when the page loads
document.addEventListener("DOMContentLoaded", setupCustomerDashboardTabs);
}

function createSalesChart(type, canvasId, labels, data, title) {
    const ctx = document.getElementById(canvasId)?.getContext("2d");
    if (!ctx) return;

    const existingChart = Chart.getChart(canvasId);
    if (existingChart) existingChart.destroy();

    new Chart(ctx, {
        type,
        data: {
            labels,
            datasets: [{
                label: title,
                data,
                backgroundColor: type === "pie" ? ["#526754", "#BC984E", "#F5F2EA", "#23645C"] : "#BC984E",
                borderColor: "#526754",
                borderWidth: 1,
            }],
        },
        options: {
            responsive: true,
            plugins: {
                legend: { position: "top" },
                title: { display: true, text: title },
            },
            scales: type === "pie" ? {} : {
                y: { beginAtZero: true },
            },
        },
    });
}

function createCustomerChart(type, canvasId, labels, data, title) {
    const ctx = document.getElementById(canvasId)?.getContext("2d");
    if (!ctx) return;

    const existingChart = Chart.getChart(canvasId);
    if (existingChart) existingChart.destroy();

    new Chart(ctx, {
        type,
        data: {
            labels,
            datasets: [{
                label: title,
                data,
                backgroundColor: "rgba(82, 103, 84, 0.7)",
                borderColor: "rgba(82, 103, 84, 1)",
                borderWidth: 1,
            }],
        },
        options: {
            responsive: true,
            plugins: {
                legend: { position: "top" },
                title: { display: true, text: title },
            },
            scales: {
                y: {
                    beginAtZero: true,
                    ticks: {
                        callback: (value) => `$${value.toLocaleString()}`,
                    },
                },
            },
        },
    });
}

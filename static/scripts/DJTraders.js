// Document Ready Listener
document.addEventListener("DOMContentLoaded", () => {
    console.log("Sales Dashboard tabs initialized.");

    if (document.querySelector(".sales-dashboard")) {
        setupSalesDashboardTabs();
        initializeChartForTab("tab-annual-overview"); // Default tab
    }
});

/* ==========================================================================
   setupSalesDashboardTabs
========================================================================== */
function setupSalesDashboardTabs() {
    const tabButtons = document.querySelectorAll(".sales-tab-button");
    const tabContents = document.querySelectorAll(".sales-tab-content");

    if (!tabButtons.length || !tabContents.length) {
        console.warn("No Sales Dashboard tabs or content found.");
        return;
    }

    tabButtons.forEach((button) => {
        button.addEventListener("click", () => {
            // Remove active class from all buttons and contents
            tabButtons.forEach((btn) => btn.classList.remove("active"));
            tabContents.forEach((content) => content.classList.remove("active"));

            // Add active class to clicked button and corresponding content
            button.classList.add("active");
            const targetTab = button.dataset.tab;
            document.getElementById(targetTab)?.classList.add("active");

            // Initialize chart for the active tab
            initializeChartForTab(targetTab);
        });
    });
}

/* ==========================================================================
   initializeChartForTab
========================================================================== */
function initializeChartForTab(tabId) {
    // Destroy existing charts for the Sales Dashboard
    ["annualSalesChart", "topProductsChart", "bottomProductsChart", "categorySalesChart"].forEach((chartId) => {
        if (Chart.getChart(chartId)) {
            Chart.getChart(chartId).destroy();
        }
    });

    switch (tabId) {
        case "tab-annual-overview":
            createAnnualSalesChart();
            break;
        case "tab-top-products":
            createTopProductsChart();
            break;
        case "tab-bottom-products":
            createBottomProductsChart();
            break;
        case "tab-category-analysis":
            createCategorySalesChart();
            break;
    }
}

/* ==========================================================================
   createAnnualSalesChart
========================================================================== */
function createAnnualSalesChart() {
    const ctx = document.getElementById("annualSalesChart")?.getContext("2d");
    if (!ctx) return;

    new Chart(ctx, {
        type: "bar",
        data: {
            labels: salesDashboardData.annualSalesLabels,
            datasets: [
                {
                    label: "Revenue",
                    data: salesDashboardData.annualSalesData,
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
                    text: "Annual Sales Overview",
                },
            },
        },
    });
}

/* ==========================================================================
   createTopProductsChart
========================================================================== */
function createTopProductsChart() {
    const ctx = document.getElementById("topProductsChart")?.getContext("2d");
    if (!ctx) return;

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
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                title: {
                    display: true,
                    text: "Top 10 Products by Revenue",
                },
            },
        },
    });
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
    if (!ctx) return;

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
}

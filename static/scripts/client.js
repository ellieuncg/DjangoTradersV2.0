document.addEventListener('DOMContentLoaded', function () {
    // Ensure dashboard data is available
    const annualSales = window.dashboardData?.annual_sales || [];
    const topProducts = window.dashboardData?.top_products || [];
    const topCategories = window.dashboardData?.top_categories || [];

    // Chart.js configuration for Annual Sales
    const annualSalesCtx = document.getElementById('annualSalesChart').getContext('2d');
    new Chart(annualSalesCtx, {
        type: 'bar',
        data: {
            labels: annualSales.map(sale => sale.order_date__year),
            datasets: [{
                label: 'Total Revenue',
                data: annualSales.map(sale => sale.total_revenue),
                backgroundColor: 'rgba(75, 192, 192, 0.6)',
                borderColor: 'rgba(75, 192, 192, 1)',
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            scales: {
                y: { beginAtZero: true }
            }
        }
    });

    // Chart.js configuration for Top Products
    const topProductsCtx = document.getElementById('topProductsChart').getContext('2d');
    new Chart(topProductsCtx, {
        type: 'pie',
        data: {
            labels: topProducts.map(product => product.product__name),
            datasets: [{
                data: topProducts.map(product => product.total_quantity),
                backgroundColor: topProducts.map((_, i) => `hsl(${i * 36}, 70%, 50%)`)
            }]
        }
    });

    // Chart.js configuration for Top Categories
    const topCategoriesCtx = document.getElementById('topCategoriesChart').getContext('2d');
    new Chart(topCategoriesCtx, {
        type: 'pie',
        data: {
            labels: topCategories.map(category => category.product__category__name),
            datasets: [{
                data: topCategories.map(category => category.total_quantity),
                backgroundColor: topCategories.map((_, i) => `hsl(${i * 36}, 70%, 50%)`)
            }]
        }
    });
});

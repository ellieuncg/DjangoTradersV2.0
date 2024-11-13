// At the very top of DJTraders.js
console.log('DJTraders.js loading...');

// Initialize when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    console.log('Document ready in DJTraders.js');
    new DjTradersApp();
});

// DjTraders main JavaScript file
class DjTradersApp {
    constructor() {
        this.successMessage = document.getElementById('successMessage');
        this.statusFilter = document.querySelector('.status-filter-header select');
        this.countryFilter = document.querySelector('.customer-search-field-header select[name="country"]');
        this.clearButton = document.querySelector('.btn-clear');
        this.customerForm = document.getElementById('customerFilterForm');
        
        // Add these new properties
        this.yearFilter = document.getElementById('yearFilter');
        this.categoryFilter = document.getElementById('categoryFilter');
        this.supplierFilter = document.getElementById('supplierFilter');

        console.log('DjTraders JS initialized');
        this.init();
    }

    init() {
        this.handleSuccessMessage();
        this.setupFilterHandlers();
        this.setupSortHandlers();
        this.updateSortIcons();
        this.setupDashboardFilters();  // Add this line
    }

    handleSuccessMessage() {
        if (this.successMessage && sessionStorage.getItem('customer_updated') === 'true') {
            console.log("Displaying success message");
            this.successMessage.style.display = 'block';
            setTimeout(() => {
                this.successMessage.style.display = 'none';
                sessionStorage.removeItem('customer_updated');
            }, 3000);
        } else {
            console.log("Success message not displayed");
        }
    }

    setupFilterHandlers() {
        // Status filter
        if (this.statusFilter) {
            this.statusFilter.addEventListener('change', () => {
                console.log('Status changed');
                this.statusFilter.form.submit();
            });
        }

        // Country filter
        if (this.countryFilter) {
            this.countryFilter.addEventListener('change', () => {
                console.log('Country changed');
                this.customerForm?.submit();
            });
        }

        // Clear filter button
        if (this.clearButton) {
            this.clearButton.addEventListener('click', (e) => this.handleClearFilter(e));
        }
    }

    handleClearFilter(e) {
        e.preventDefault();
        const currentUrl = new URL(window.location.href);
        const status = currentUrl.searchParams.get('status') || 'active';
        const baseUrl = window.location.pathname;
        
        window.location.href = `${baseUrl}?status=${status}`;
    }

    setupSortHandlers() {
        document.querySelectorAll('.sort-icon').forEach(icon => {
            icon.addEventListener('click', () => this.handleSort(icon));
        });
    }

    handleSort(icon) {
        console.log('Sort icon clicked');
        const field = icon.getAttribute('data-sort');
        const currentUrl = new URL(window.location.href);
        const params = currentUrl.searchParams;
        
        // Get current sort field and direction
        const currentSort = params.get('sort') || '';
        const currentDirection = params.get('direction') || 'asc';
        
        // Determine new sort direction
        const newDirection = field === currentSort && currentDirection === 'asc' ? 'desc' : 'asc';
        
        // Update parameters
        this.updateSortParameters(params, field, newDirection);
        
        console.log('New URL:', currentUrl.toString());
        window.location.href = currentUrl.toString();
    }

    updateSortParameters(params, field, direction) {
        // Add form values if customer form exists
        if (this.customerForm) {
            const formData = new FormData(this.customerForm);
            for (let [key, value] of formData.entries()) {
                if (value) {
                    params.set(key, value);
                }
            }
        }
        
        // Set sort parameters
        params.set('sort', field);
        params.set('direction', direction);
        
        // Preserve status filter
        const statusSelect = document.querySelector('.status-select');
        if (statusSelect?.value) {
            params.set('status', statusSelect.value);
        }
        
        // Preserve letter filter
        const letter = params.get('letter');
        if (letter) {
            params.set('letter', letter);
        }
    }

    updateSortIcons() {
        const params = new URLSearchParams(window.location.search);
        const currentSort = params.get('sort');
        const currentDirection = params.get('direction');

        document.querySelectorAll('.sort-icon').forEach(icon => {
            const field = icon.getAttribute('data-sort');
            icon.classList.remove('fa-sort', 'fa-sort-up', 'fa-sort-down');
            
            if (field === currentSort) {
                icon.classList.add(currentDirection === 'asc' ? 'fa-sort-up' : 'fa-sort-down');
            } else {
                icon.classList.add('fa-sort');
            }
        });
    }

    setupDashboardFilters() {
        // Setup year filter
        if (this.yearFilter) {
            console.log('Setting up year filter');
            this.yearFilter.addEventListener('change', () => this.filterDashboard());
        }

        // Setup category filter
        if (this.categoryFilter) {
            console.log('Setting up category filter');
            this.categoryFilter.addEventListener('change', () => this.filterDashboard());
        }

        // Setup supplier filter
        if (this.supplierFilter) {
            console.log('Setting up supplier filter');
            this.supplierFilter.addEventListener('change', () => this.filterDashboard());
        }
    }

    filterDashboard() {
        const year = this.yearFilter?.value || '';
        const category = this.categoryFilter?.value || '';
        const supplier = this.supplierFilter?.value || '';
    
        console.log(`Filtering with - Year: ${year}, Category: ${category}, Supplier: ${supplier}`);
    
        const url = `/sales/dashboard/?year=${year}&category=${category}&supplier=${supplier}`;
        
        fetch(url, {
            headers: {
                'X-Requested-With': 'XMLHttpRequest'
            }
        })
        .then(response => response.json())
        .then(data => {
            console.log('Received filtered data:', data);
            this.updateDashboard(data);
        })
        .catch(error => console.error('Error fetching filtered data:', error));
    }
    
    

    updateDashboard(data) {
        console.log("Update dashboard with data:", data);
        // You would implement the actual logic here to update the DOM
        // based on the data received from the AJAX call.
    }
}

$(document).ready(function() {
    console.log('jQuery ready!');

    $('#yearFilter, #categoryFilter, #supplierFilter').on('change', function() {
        console.log('Filter changed');
        
        var year = $('#yearFilter').val();
        var category = $('#categoryFilter').val();
        var supplier = $('#supplierFilter').val();
        
        var url = window.location.pathname + '?year=' + year;
        if (category) {
            url += '&category=' + category;
        }
        if (supplier) {
            url += '&supplier=' + supplier;
        }
        
        console.log('Going to URL:', url);
        window.location.href = url;
    });
});
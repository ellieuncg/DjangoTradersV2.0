// DJTraders.js
console.log('DJTraders.js loading...');

document.addEventListener('DOMContentLoaded', () => {
    console.log('Document ready in DJTraders.js');
    new DjTradersApp();
    setupCustomerDashboardTabs(); // Call the function to set up tabs
});

class DjTradersApp {
    constructor() {
        this.initializeElements();
        console.log('DjTraders JS initialized');
        this.init();
    }

    initializeElements() {
        // Dashboard filters
        this.yearFilter = document.getElementById('yearFilter');
        this.categoryFilter = document.getElementById('categoryFilter');
        this.supplierFilter = document.getElementById('supplierFilter');
        
        // Customer management elements
        this.successMessage = document.getElementById('successMessage');
        this.statusFilter = document.querySelector('.status-filter-header select');
        this.countryFilter = document.querySelector('.customer-search-field-header select[name="country"]');
        this.clearButton = document.querySelector('.btn-clear');
        this.customerForm = document.getElementById('customerFilterForm');
    }

    init() {
        this.handleSuccessMessage();
        this.setupFilterHandlers();
        this.setupSortHandlers();
        this.updateSortIcons();
        this.setupDashboardFilters();
    }

    handleSuccessMessage() {
        if (this.successMessage && sessionStorage.getItem('customer_updated') === 'true') {
            console.log("Displaying success message");
            this.successMessage.style.display = 'block';
            setTimeout(() => {
                this.successMessage.style.display = 'none';
                sessionStorage.removeItem('customer_updated');
            }, 3000);
        }
    }

    setupFilterHandlers() {
        if (this.statusFilter) {
            this.statusFilter.addEventListener('change', () => {
                console.log('Status changed');
                this.statusFilter.form.submit();
            });
        }

        if (this.countryFilter) {
            this.countryFilter.addEventListener('change', () => {
                console.log('Country changed');
                this.customerForm?.submit();
            });
        }

        if (this.clearButton) {
            this.clearButton.addEventListener('click', (e) => this.handleClearFilter(e));
        }
    }

    setupDashboardFilters() {
        const filters = [this.yearFilter, this.categoryFilter, this.supplierFilter];
        
        filters.forEach(filter => {
            if (filter) {
                console.log(`Setting up ${filter.id}`);
                filter.addEventListener('change', () => this.handleDashboardFilter());
            }
        });
    }

    handleDashboardFilter() {
        const year = this.yearFilter?.value || '';
        const category = this.categoryFilter?.value || '';
        const supplier = this.supplierFilter?.value || '';
    
        console.log(`Filtering with - Year: ${year}, Category: ${category}, Supplier: ${supplier}`);
    
        const url = `${window.location.pathname}?year=${year}${category ? '&category=' + category : ''}${supplier ? '&supplier=' + supplier : ''}`;
        window.location.href = url;
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
        const field = icon.getAttribute('data-sort');
        const currentUrl = new URL(window.location.href);
        const params = currentUrl.searchParams;
        
        const currentSort = params.get('sort') || '';
        const currentDirection = params.get('direction') || 'asc';
        const newDirection = field === currentSort && currentDirection === 'asc' ? 'desc' : 'asc';
        
        this.updateSortParameters(params, field, newDirection);
        window.location.href = currentUrl.toString();
    }

    updateSortParameters(params, field, direction) {
        if (this.customerForm) {
            const formData = new FormData(this.customerForm);
            for (let [key, value] of formData.entries()) {
                if (value) params.set(key, value);
            }
        }
        
        params.set('sort', field);
        params.set('direction', direction);
        
        const statusSelect = document.querySelector('.status-select');
        if (statusSelect?.value) {
            params.set('status', statusSelect.value);
        }
        
        const letter = params.get('letter');
        if (letter) params.set('letter', letter);
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
}

// Tab setup for the customer dashboard
function setupCustomerDashboardTabs() {
    const tabButtons = document.querySelectorAll('.customer-tab-button');
    const tabContents = document.querySelectorAll('.customer-tab-content');

    console.log('Setting up tab buttons...');
    tabButtons.forEach(button => {
        button.addEventListener('click', () => {
            console.log(`Clicked tab: ${button.dataset.tab}`);
            
            // Remove active class from all buttons and contents
            tabButtons.forEach(btn => btn.classList.remove('active'));
            tabContents.forEach(content => content.classList.remove('active'));

            // Add active class to the clicked button and corresponding content
            button.classList.add('active');
            const content = document.getElementById(button.dataset.tab);
            if (content) {
                content.classList.add('active');
                console.log(`Activating content: ${button.dataset.tab}`);
            } else {
                console.log(`Content for ${button.dataset.tab} not found`);
            }
        });
    });
}

document.addEventListener('DOMContentLoaded', () => {
    console.log('Document ready in DJTraders.js');
    new DjTradersApp();
    setupCustomerDashboardTabs(); // Call the function to set up tabs
});

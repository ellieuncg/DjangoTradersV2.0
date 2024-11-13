// DjTraders main JavaScript file
class DjTradersApp {
    constructor() {
        this.successMessage = document.getElementById('successMessage');
        this.statusFilter = document.querySelector('.status-filter-header select');
        this.countryFilter = document.querySelector('.customer-search-field-header select[name="country"]');
        this.clearButton = document.querySelector('.btn-clear');
        this.customerForm = document.getElementById('customerFilterForm');

        console.log('DjTraders JS initialized');
        this.init();
    }

    init() {
        this.handleSuccessMessage();
        this.setupFilterHandlers();
        this.setupSortHandlers();
        this.updateSortIcons();
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
}

// Initialize when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    console.log('Document ready');
    new DjTradersApp();
});
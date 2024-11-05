console.log('DjTraders JS file loaded');

document.addEventListener('DOMContentLoaded', function() {
    console.log('Document ready');

    // Show success message if it exists
    const successMessage = document.getElementById('successMessage');
    if (successMessage && sessionStorage.getItem('customer_updated') === 'true') {
        console.log("Displaying success message");  // Debug log
        successMessage.style.display = 'block';
        setTimeout(() => {
            successMessage.style.display = 'none';
            sessionStorage.removeItem('customer_updated');  // Clear session flag
        }, 3000); // Hide after 3 seconds
    } else {
        console.log("Success message not displayed");  // Debug log
    }

    // Status filter change handler
    const statusFilter = document.querySelector('.status-filter-header select');
    if (statusFilter) {
        statusFilter.addEventListener('change', function() {
            console.log('Status changed');
            this.form.submit();
        });
    }

    // Country filter change handler
    const countryFilter = document.querySelector('.customer-search-field-header select[name="country"]');
    if (countryFilter) {
        countryFilter.addEventListener('change', function() {
            console.log('Country changed');
            document.getElementById('customerFilterForm').submit();
        });
    }

    // Clear button handler
    const clearButton = document.querySelector('.btn-clear');
    if (clearButton) {
        clearButton.addEventListener('click', function(e) {
            e.preventDefault();
            const currentUrl = new URL(window.location.href);
            const status = currentUrl.searchParams.get('status') || 'active';
            const baseUrl = window.location.pathname;
            
            // Redirect to base URL with only status parameter
            window.location.href = `${baseUrl}?status=${status}`;
        });
    }

    // Sort icon click handlers
    document.querySelectorAll('.sort-icon').forEach(icon => {
        icon.addEventListener('click', function() {
            console.log('Sort icon clicked');
            const field = this.getAttribute('data-sort');
            const currentUrl = new URL(window.location.href);
            const params = currentUrl.searchParams;
            
            // Get current sort field and direction
            let currentSort = params.get('sort') || '';
            let currentDirection = params.get('direction') || 'asc';
            
            // Determine new sort direction
            let newDirection = 'asc';
            if (field === currentSort) {
                newDirection = currentDirection === 'asc' ? 'desc' : 'asc';
            }
            
            // Get all current form values if customer form exists
            const customerForm = document.getElementById('customerFilterForm');
            if (customerForm) {
                const formData = new FormData(customerForm);
                // Update URL parameters while preserving search form values
                for (let [key, value] of formData.entries()) {
                    if (value) {  // Only add parameters that have values
                        params.set(key, value);
                    }
                }
            }
            
            // Add sort parameters
            params.set('sort', field);
            params.set('direction', newDirection);
            
            // Preserve status filter if exists
            const statusSelect = document.querySelector('.status-select');
            if (statusSelect) {
                const status = statusSelect.value;
                if (status) {
                    params.set('status', status);
                }
            }
            
            // Preserve letter filter if exists
            const letter = params.get('letter');
            if (letter) {
                params.set('letter', letter);
            }
            
            console.log('New URL:', currentUrl.toString());
            
            // Update the URL and reload page
            window.location.href = currentUrl.toString();
        });
    });

    // Initialize sort icons based on current URL parameters
    function updateSortIcons() {
        const params = new URLSearchParams(window.location.search);
        const currentSort = params.get('sort');
        const currentDirection = params.get('direction');

        document.querySelectorAll('.sort-icon').forEach(function(icon) {
            const field = icon.getAttribute('data-sort');
            if (field === currentSort) {
                icon.classList.remove('fa-sort');
                icon.classList.add(currentDirection === 'asc' ? 'fa-sort-up' : 'fa-sort-down');
            } else {
                icon.classList.remove('fa-sort-up', 'fa-sort-down');
                icon.classList.add('fa-sort');
            }
        });
    }

    // Call updateSortIcons when page loads
    updateSortIcons();
});

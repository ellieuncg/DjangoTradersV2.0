console.log('DjTraders JS file loaded');

$(document).ready(function() {
    console.log('jQuery loaded and document ready');

    // Status filter change handler
    $('.status-filter-header select').on('change', function() {
        console.log('Status changed');
        this.form.submit();
    });

    // Clear button handler
    $('.btn-clear').on('click', function(e) {
        e.preventDefault();
        const currentUrl = new URL(window.location.href);
        const status = currentUrl.searchParams.get('status') || 'active';
        const baseUrl = window.location.pathname;
        
        // Redirect to base URL with only status parameter
        window.location.href = `${baseUrl}?status=${status}`;
    });

    // Sort icon click handler
    $('.sort-icon').on('click', function() {
        console.log('Sort icon clicked');
        const field = $(this).data('sort');
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

    // Initialize sort icons based on current URL parameters
    function updateSortIcons() {
        const params = new URLSearchParams(window.location.search);
        const currentSort = params.get('sort');
        const currentDirection = params.get('direction');

        $('.sort-icon').each(function() {
            const field = $(this).data('sort');
            if (field === currentSort) {
                $(this).removeClass('fa-sort')
                    .addClass(currentDirection === 'asc' ? 'fa-sort-up' : 'fa-sort-down');
            } else {
                $(this).removeClass('fa-sort-up fa-sort-down').addClass('fa-sort');
            }
        });
    }

    // Call updateSortIcons when page loads
    updateSortIcons();
});
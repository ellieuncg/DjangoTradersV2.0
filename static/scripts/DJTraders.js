// Main JavaScript file for Django Traders
$(document).ready(function() {
    const djTraders = new DJTraders();
});

class DJTraders {
    constructor() {
        this.initializeComponents();
        this.setupEventListeners();
    }

    initializeComponents() {
        // Initialize DataTables
        this.initializeDataTables();
        
        // Initialize tooltips
        this.initializeTooltips();
        
        // Initialize action buttons
        this.initializeActionButtons();
    }

    initializeDataTables() {
        const dataTableConfig = {
            order: [0, 'asc'],
            responsive: true,
            pageLength: 10,
            language: {
                search: "Filter results:",
                zeroRecords: "No records found",
                paginate: {
                    next: "Next",
                    previous: "Previous"
                }
            },
            drawCallback: () => {
                this.initializeActionButtons();
            }
        };

        $('.data-table').each(function() {
            $(this).DataTable(dataTableConfig);
        });
    }

    initializeTooltips() {
        $('[data-bs-toggle="tooltip"]').tooltip();
    }

    initializeActionButtons() {
        $('.action-btn').each((_, btn) => {
            const $btn = $(btn);
            if (!$btn.data('initialized')) {
                $btn.on('click', (e) => this.handleActionButton(e, $btn));
                $btn.data('initialized', true);
            }
        });
    }

    setupEventListeners() {
        // Form submission
        $('form').on('submit', (e) => this.handleFormSubmit(e));

        // Dynamic search
        $('.search-input').on('input', this.debounce((e) => {
            this.handleSearch($(e.target));
        }, 300));

        // Filter buttons
        $('.filter-btn').on('click', (e) => this.handleFilter(e));
    }

    handleActionButton(e, $btn) {
        if ($btn.data('confirm')) {
            if (!confirm($btn.data('confirm'))) {
                e.preventDefault();
                return false;
            }
        }

        if ($btn.data('action')) {
            e.preventDefault();
            this.performAction($btn);
        }
    }

    handleFormSubmit(e) {
        const $form = $(e.target);
        
        if (!this.validateForm($form)) {
            e.preventDefault();
            return false;
        }
    }

    handleSearch($input) {
        const query = $input.val();
        const url = $input.data('search-url') || window.location.pathname;
        
        this.performSearch(url, query);
    }

    handleFilter(e) {
        e.preventDefault();
        const $btn = $(e.target);
        const filter = $btn.data('filter');
        
        $('.filter-btn').removeClass('active');
        $btn.addClass('active');
        
        this.applyFilter(filter);
    }

    validateForm($form) {
        let isValid = true;
        
        // Clear previous errors
        $('.error-message').remove();
        $('.has-error').removeClass('has-error');

        // Required fields
        $form.find('[required]').each((_, element) => {
            if (!$(element).val()) {
                isValid = false;
                this.showError($(element), 'This field is required');
            }
        });

        // Numeric fields
        $form.find('[type="number"]').each((_, element) => {
            const $element = $(element);
            const val = $element.val();
            const min = $element.attr('min');
            const max = $element.attr('max');
            
            if (val && (
                (min && parseFloat(val) < parseFloat(min)) ||
                (max && parseFloat(val) > parseFloat(max))
            )) {
                isValid = false;
                this.showError($element, `Value must be between ${min} and ${max}`);
            }
        });

        return isValid;
    }

    showError($element, message) {
        $element.addClass('has-error')
            .after(`<div class="error-message">${message}</div>`);
    }

    debounce(func, wait) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    }

    performSearch(url, query) {
        $.get(url, { q: query }, (response) => {
            // Update the results container with the response
            $('.results-container').html(response);
        });
    }

    applyFilter(filter) {
        const currentUrl = new URL(window.location.href);
        currentUrl.searchParams.set('filter', filter);
        window.location.href = currentUrl.toString();
    }
}
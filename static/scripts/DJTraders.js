// Main JavaScript file for Django Traders
$(document).ready(function() {
    const djTraders = new DJTraders();
});

class DJTraders {
    constructor() {
        this.currentSort = {
            field: null,
            direction: null
        };
        this.initializeComponents();
        this.setupEventListeners();
    }

    initializeComponents() {
        // Initialize tooltips
        this.initializeTooltips();
        
        // Initialize action buttons
        this.initializeActionButtons();

        // Highlight active letter in alphabetical navigation
        this.highlightActiveLetter();

        // Highlight active category in category navigation
        this.highlightActiveCategory();
    }

    highlightActiveLetter() {
        // Only run on the Customers page by checking the URL
        if (!window.location.href.includes('Customers')) return;
    
        // Get the URL parameters
        const urlParams = new URLSearchParams(window.location.search);
        const selectedLetter = urlParams.get('letter');
        console.log("Selected letter from URL:", selectedLetter);
    
        // Select all alphabetical links
        const alphaLinks = document.querySelectorAll('.alphabet-links-customers a');
    
        // Loop through each link and add active class if it matches the selected letter
        alphaLinks.forEach(link => {
            if (link.textContent.trim() === selectedLetter) {
                link.classList.add('active');
                console.log("Adding active class to:", link.textContent);
            } else {
                link.classList.remove('active');
            }
        });
    
        // If no letter is selected (e.g., "All" link), apply the active class to "All"
        if (!selectedLetter) {
            const allLink = document.querySelector('.alphabet-links-customers a:first-child');
            allLink.classList.add('active');
            console.log("Adding active class to 'All' link");
        }
    }

    highlightActiveCategory() {
        // Only run on the Products page by checking the URL
        if (!window.location.href.includes('Products')) return;

        // Get the URL parameters
        const urlParams = new URLSearchParams(window.location.search);
        const selectedCategory = urlParams.get('category');
        console.log("Selected category from URL:", selectedCategory);

        // Select all category links
        const categoryLinks = document.querySelectorAll('.categories-wrapper-products a');

        // Loop through each link and add active class if it matches the selected category
        categoryLinks.forEach(link => {
            if (link.getAttribute('href').includes(`category=${selectedCategory}`)) {
                link.classList.add('active');
                console.log("Adding active class to:", link.textContent);
            } else {
                link.classList.remove('active');
            }
        });

        // If no category is selected (e.g., "All Categories" link), apply the active class to "All Categories"
        if (!selectedCategory) {
            const allLink = document.querySelector('.categories-wrapper-products a:first-child');
            allLink.classList.add('active');
            console.log("Adding active class to 'All Categories' link");
        }
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

        // Status select dropdown
        $('.status-select').on('change', (e) => {
            if (!$(e.target).hasClass('sort-control')) {
                e.target.form.submit();
            }
        });

        // Clear button
        $('.clear-search-btn').on('click', () => this.clearSearch());

        // Sort icon click handler
        $('.sort-icon').on('click', (e) => this.handleSortClick(e));
    }

    handleSortClick(e) {
        const $icon = $(e.currentTarget);
        const field = $icon.data('sort');
        
        // Toggle sort direction or set initial direction
        if (this.currentSort.field === field) {
            this.currentSort.direction = this.currentSort.direction === 'asc' ? 'desc' : 'asc';
        } else {
            this.currentSort.field = field;
            this.currentSort.direction = 'asc';
        }

        // Update icon states
        $('.sort-icon').removeClass('active-asc active-desc');
        $icon.addClass(`active-${this.currentSort.direction}`);

        // Perform the sort
        this.sortCards();
    }

    sortCards() {
        const $container = $('.card-grid-products, .card-grid-customers');
        const $cards = $container.children().toArray();
        const field = this.currentSort.field;
        const direction = this.currentSort.direction;

        $cards.sort((a, b) => {
            const aVal = this.getSortValue($(a), field);
            const bVal = this.getSortValue($(b), field);

            if (field === 'price') {
                const aNum = parseFloat(aVal);
                const bNum = parseFloat(bVal);
                return direction === 'asc' ? aNum - bNum : bNum - aNum;
            }

            return direction === 'asc' ? 
                aVal.localeCompare(bVal) : 
                bVal.localeCompare(aVal);
        });

        $container.append($cards);
    }

    getSortValue($card, field) {
        switch (field) {
            case 'product':
                return $card.find('.card-title').text().trim();
            case 'supplier':
                return $card.find('strong:contains("Supplier")').parent().text().split(':')[1].trim();
            case 'price':
                const priceText = $card.find('strong:contains("Unit Price")').parent().text();
                return priceText.replace(/[^0-9.-]+/g, '');
            case 'customer':
                return $card.find('.card-title').text().trim();
            case 'contact':
                return $card.find('strong:contains("Contact")').parent().text().split(':')[1].trim();
            case 'city':
                return $card.find('strong:contains("City")').parent().text().split(':')[1].trim();
            case 'country':
                return $card.find('strong:contains("Country")').parent().text().split(':')[1].trim();
            default:
                return '';
        }
    }

    clearSearch() {
        // Get current URL without parameters
        const baseUrl = window.location.pathname;
        // Redirect to base URL
        window.location.href = baseUrl;
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

    performAction($btn) {
        const action = $btn.data('action');
        const url = $btn.data('url');
        const method = $btn.data('method') || 'POST';
        
        $.ajax({
            url: url,
            method: method,
            success: (response) => {
                if (response.redirect) {
                    window.location.href = response.redirect;
                } else {
                    location.reload();
                }
            },
            error: (xhr) => {
                alert('An error occurred. Please try again.');
            }
        });
    }
}
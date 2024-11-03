$(document).ready(function() {
    console.log('jQuery loaded and document ready');
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
        this.initializeTooltips();
        this.initializeActionButtons();
        this.highlightActiveLetter();
        this.highlightActiveCategory();
    }

    highlightActiveLetter() {
        if (!window.location.href.includes('Customers')) return;
        
        const urlParams = new URLSearchParams(window.location.search);
        const selectedLetter = urlParams.get('letter');
        const alphaLinks = document.querySelectorAll('.alphabet-links-customers a');
        
        alphaLinks.forEach(link => {
            if (link.textContent.trim() === selectedLetter) {
                link.classList.add('active');
            } else {
                link.classList.remove('active');
            }
        });

        if (!selectedLetter) {
            const allLink = document.querySelector('.alphabet-links-customers a:first-child');
            if (allLink) allLink.classList.add('active');
        }
    }

    highlightActiveCategory() {
        if (!window.location.href.includes('Products')) return;
        
        const urlParams = new URLSearchParams(window.location.search);
        const selectedCategory = urlParams.get('category');
        const categoryLinks = document.querySelectorAll('.categories-wrapper-products a');
        
        categoryLinks.forEach(link => {
            if (link.getAttribute('href').includes(`category=${selectedCategory}`)) {
                link.classList.add('active');
            } else {
                link.classList.remove('active');
            }
        });

        if (!selectedCategory) {
            const allLink = document.querySelector('.categories-wrapper-products a:first-child');
            if (allLink) allLink.classList.add('active');
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
        $('form').on('submit', (e) => this.handleFormSubmit(e));
        
        $('.status-select').on('change', (e) => {
            if (!$(e.target).hasClass('sort-control')) {
                e.target.form.submit();
            }
        });

        // Clear button
        $('.clear-search-btn').on('click', (e) => {
            e.preventDefault();
            this.clearSearch();
        });

        // Sort icon click handler
        $('.sort-icon').on('click', (e) => this.handleSortClick(e));
    }

    handleSortClick(e) {
        console.log('Sort clicked!');
        const $icon = $(e.currentTarget);
        const field = $icon.data('sort');
        console.log('Sorting by:', field);

        if (this.currentSort.field === field) {
            this.currentSort.direction = this.currentSort.direction === 'asc' ? 'desc' : 'asc';
        } else {
            this.currentSort.field = field;
            this.currentSort.direction = 'asc';
        }

        $('.sort-icon').removeClass('active-asc active-desc');
        $icon.addClass(`active-${this.currentSort.direction}`);

        this.sortCards();
    }

    sortCards() {
        console.log('Sorting cards...');
        const $container = $('.card-grid-products, .card-grid-customers');
        const $cards = $container.children().toArray();
        
        if ($cards.length === 0) {
            console.log('No cards found to sort');
            return;
        }

        console.log(`Sorting ${$cards.length} cards by ${this.currentSort.field} in ${this.currentSort.direction} order`);

        $cards.sort((a, b) => {
            const aVal = this.getSortValue($(a), this.currentSort.field);
            const bVal = this.getSortValue($(b), this.currentSort.field);

            if (this.currentSort.field === 'price') {
                return this.currentSort.direction === 'asc' ? aVal - bVal : bVal - aVal;
            }

            return this.currentSort.direction === 'asc' ? 
                String(aVal).localeCompare(String(bVal)) : 
                String(bVal).localeCompare(String(aVal));
        });

        $container.empty().append($cards);
    }

    getSortValue($card, field) {
        switch (field) {
            case 'product':
                return $card.find('.card-title').text().trim();
            case 'supplier':
                const supplierText = $card.find('p:contains("Supplier:")').text();
                return supplierText ? supplierText.split(':')[1].trim() : '';
            case 'price':
                const priceText = $card.find('p:contains("Unit Price:")').text();
                const priceMatch = priceText.match(/\$?([\d.]+)/);
                return priceMatch ? parseFloat(priceMatch[1]) : 0;
            default:
                return '';
        }
    }

    clearSearch() {
        console.log('Clear button clicked');
        
        const currentUrl = new URL(window.location.href);
        const status = currentUrl.searchParams.get('status') || 'active';
        const baseUrl = window.location.pathname;
        
        let newUrl = baseUrl + '?status=' + status;
        
        if (window.location.href.includes('customers')) {
            const letter = currentUrl.searchParams.get('letter');
            if (letter) {
                newUrl += '&letter=' + letter;
            }
        }
        
        window.location.href = newUrl;
    }

    handleActionButton(e, $btn) {
        if ($btn.data('confirm') && !confirm($btn.data('confirm'))) {
            e.preventDefault();
            return false;
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

    validateForm($form) {
        let isValid = true;
        $('.error-message').remove();
        $('.has-error').removeClass('has-error');

        $form.find('[required]').each((_, element) => {
            if (!$(element).val()) {
                isValid = false;
                this.showError($(element), 'This field is required');
            }
        });

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

    performAction($btn) {
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
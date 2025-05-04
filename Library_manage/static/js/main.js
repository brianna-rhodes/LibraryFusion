// Book Search Functionality
document.addEventListener('DOMContentLoaded', function() {
    // Initialize tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Book search form submission
    const searchForm = document.querySelector('.search-form');
    if (searchForm) {
        searchForm.addEventListener('submit', function(e) {
            const searchInput = this.querySelector('input[type="text"]');
            const categorySelect = this.querySelector('select[name="category"]');
            
            if (!searchInput.value.trim() && !categorySelect.value) {
                e.preventDefault();
                searchInput.focus();
            }
        });
    }

    // Google Books search form submission
    const googleBooksForm = document.getElementById('googleBooksSearchForm');
    if (googleBooksForm) {
        googleBooksForm.addEventListener('submit', function(e) {
            e.preventDefault();
            const searchInput = document.getElementById('bookSearch');
            const categorySelect = document.querySelector('select[name="category"]');
            const searchQuery = searchInput.value.trim();
            const category = categorySelect ? categorySelect.value : '';
            
            if (searchQuery || category) {
                fetch(`/books/search/?q=${encodeURIComponent(searchQuery)}&category=${encodeURIComponent(category)}`, {
                    method: 'GET',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': getCookie('csrftoken')
                    }
                })
                .then(response => response.json())
                .then(data => {
                    const resultsBody = document.getElementById('searchResultsBody');
                    resultsBody.innerHTML = '';
                    
                    if (data.books && data.books.length > 0) {
                        data.books.forEach(book => {
                            const row = document.createElement('tr');
                            row.innerHTML = `
                                <td>${book.title}</td>
                                <td>${book.authors.join(', ')}</td>
                                <td>${book.isbn || 'N/A'}</td>
                                <td>${book.categories ? book.categories.join(', ') : 'N/A'}</td>
                                <td>
                                    <button class="btn btn-sm btn-primary import-book" 
                                            data-book='${JSON.stringify(book)}'>
                                        Import
                                    </button>
                                </td>
                            `;
                            resultsBody.appendChild(row);
                        });
                        document.getElementById('searchResults').classList.remove('d-none');
                    } else {
                        resultsBody.innerHTML = '<tr><td colspan="5" class="text-center">No results found</td></tr>';
                        document.getElementById('searchResults').classList.remove('d-none');
                    }
                })
                .catch(error => {
                    console.error('Error:', error);
                    const resultsBody = document.getElementById('searchResultsBody');
                    resultsBody.innerHTML = '<tr><td colspan="5" class="text-center text-danger">Error searching for books</td></tr>';
                    document.getElementById('searchResults').classList.remove('d-none');
                });
            }
        });
    }

    // Star rating functionality
    const starRatings = document.querySelectorAll('.star-rating');
    starRatings.forEach(rating => {
        const stars = rating.querySelectorAll('.star');
        stars.forEach((star, index) => {
            star.addEventListener('click', () => {
                stars.forEach((s, i) => {
                    if (i <= index) {
                        s.classList.add('active');
                    } else {
                        s.classList.remove('active');
                    }
                });
            });
        });
    });

    // Mobile menu toggle
    const mobileMenuToggle = document.querySelector('.navbar-toggler');
    if (mobileMenuToggle) {
        mobileMenuToggle.addEventListener('click', function() {
            document.body.classList.toggle('menu-open');
        });
    }

    // Book availability status
    const availabilityBadges = document.querySelectorAll('.availability-badge');
    availabilityBadges.forEach(badge => {
        const status = badge.dataset.status;
        if (status === 'available') {
            badge.classList.add('bg-success');
        } else if (status === 'borrowed') {
            badge.classList.add('bg-warning');
        } else {
            badge.classList.add('bg-danger');
        }
    });

    // Fine calculation
    const fineElements = document.querySelectorAll('.fine-amount');
    fineElements.forEach(element => {
        const amount = parseFloat(element.dataset.amount);
        if (amount > 0) {
            element.classList.add('text-danger');
        }
    });

    // Form validation
    const forms = document.querySelectorAll('.needs-validation');
    forms.forEach(form => {
        form.addEventListener('submit', function(event) {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }
            form.classList.add('was-validated');
        }, false);
    });
}); 

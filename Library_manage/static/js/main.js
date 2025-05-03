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
            const searchInput = this.querySelector('input[type="search"]');
            if (!searchInput.value.trim()) {
                e.preventDefault();
                searchInput.focus();
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
}); ('.star-rating');
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

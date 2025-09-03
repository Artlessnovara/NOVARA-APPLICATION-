document.addEventListener('DOMContentLoaded', function() {
    const searchInput = document.getElementById('search-input');
    const clearButton = document.getElementById('clear-search-btn');

    if (clearButton && searchInput) {
        clearButton.addEventListener('click', function(event) {
            // Prevent the link from navigating if it's an anchor tag
            event.preventDefault();

            // Clear the input field
            searchInput.value = '';

            // Optionally, you could redirect to the clean search page
            window.location.href = this.href;
        });
    }
});

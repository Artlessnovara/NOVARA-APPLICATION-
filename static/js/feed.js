document.addEventListener('DOMContentLoaded', function() {
    document.body.addEventListener('click', function(event) {
        if (event.target.matches('.like-btn')) {
            event.preventDefault();
            const button = event.target;
            const postId = button.dataset.postId;
            const url = `/like/${postId}`;

            fetch(url, {
                method: 'POST',
                headers: {
                    // We might need a CSRF token here if the app uses it for POST requests.
                    // For now, assuming session cookie is enough for authentication.
                    'Content-Type': 'application/json'
                }
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    // Update the like count
                    const likeCountSpan = button.closest('.engagement-row').querySelector('.like-count');
                    if (likeCountSpan) {
                        likeCountSpan.textContent = data.likes_count;
                    }

                    // Toggle the button's appearance (e.g., color)
                    if (data.liked) {
                        button.classList.add('text-primary');
                        button.classList.remove('text-muted');
                    } else {
                        button.classList.remove('text-primary');
                        button.classList.add('text-muted');
                    }
                }
            })
            .catch(error => console.error('Error:', error));
        }
    });
});

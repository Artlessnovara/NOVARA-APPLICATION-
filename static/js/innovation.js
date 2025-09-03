document.addEventListener('DOMContentLoaded', function() {
    document.body.addEventListener('click', function(event) {
        const button = event.target.closest('.support-btn');

        if (button) {
            event.preventDefault();
            const projectId = button.dataset.projectId;
            const url = `/project/${projectId}/toggle_support`;

            fetch(url, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                }
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    // Update the supporter count
                    const supporterCountSpan = button.closest('.card-body').querySelector('.supporter-count');
                    if (supporterCountSpan) {
                        supporterCountSpan.textContent = data.supporter_count;
                    }

                    // Toggle the button's appearance
                    if (data.is_supporter) {
                        button.textContent = 'Supported';
                        button.classList.remove('btn-outline-primary');
                        button.classList.add('btn-primary');
                    } else {
                        button.textContent = 'Support';
                        button.classList.remove('btn-primary');
                        button.classList.add('btn-outline-primary');
                    }
                }
            })
            .catch(error => console.error('Error:', error));
        }
    });
});

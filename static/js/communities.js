document.addEventListener('DOMContentLoaded', function() {
    document.body.addEventListener('click', function(event) {
        // Use .closest() to catch clicks on the icon inside the button too
        const button = event.target.closest('.join-leave-btn');

        if (button) {
            event.preventDefault();
            const communityId = button.dataset.communityId;
            const url = `/community/${communityId}/toggle_join`;

            fetch(url, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                }
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    // Update the member count
                    const memberCountSpan = button.closest('.card-body').querySelector('.member-count');
                    if (memberCountSpan) {
                        memberCountSpan.textContent = data.member_count;
                    }

                    // Toggle the button's appearance
                    if (data.is_member) {
                        button.textContent = 'Joined';
                        button.classList.remove('btn-success');
                        button.classList.add('btn-secondary');
                    } else {
                        button.textContent = 'Join';
                        button.classList.remove('btn-secondary');
                        button.classList.add('btn-success');
                    }
                }
            })
            .catch(error => console.error('Error:', error));
        }
    });
});

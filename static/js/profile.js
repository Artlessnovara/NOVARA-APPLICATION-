document.addEventListener('DOMContentLoaded', function() {
    const followBtn = document.getElementById('follow-btn');

    if (followBtn) {
        followBtn.addEventListener('click', function() {
            const userId = this.dataset.userId;
            const url = `/user/${userId}/toggle_follow`;

            fetch(url, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    // In a real app with CSRF protection, you'd include the token here
                }
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    // Update follower count
                    const followersCountEl = document.getElementById('followers-count');
                    followersCountEl.textContent = data.followers_count;

                    // Update button appearance and text
                    if (data.is_following) {
                        this.textContent = 'Unfollow';
                        this.classList.remove('btn-primary');
                        this.classList.add('btn-secondary');
                    } else {
                        this.textContent = 'Follow';
                        this.classList.remove('btn-secondary');
                        this.classList.add('btn-primary');
                    }
                } else {
                    // Optionally, handle the error case, e.g., show an alert
                    console.error('Follow/unfollow action failed:', data.message);
                }
            })
            .catch(error => console.error('Error:', error));
        });
    }
});

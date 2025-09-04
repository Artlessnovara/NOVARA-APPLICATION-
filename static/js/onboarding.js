document.addEventListener('DOMContentLoaded', function() {
    const getStartedBtn = document.getElementById('get-started-btn');

    if (getStartedBtn) {
        getStartedBtn.addEventListener('click', function() {
            // Set a flag in localStorage so the user doesn't see this again
            localStorage.setItem('hasSeenOnboarding', 'true');
            // Redirect to the main landing page, which will then route to home/login
            window.location.href = "/";
        });
    }
});

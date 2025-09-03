document.addEventListener('DOMContentLoaded', function() {
    const storiesContainer = document.getElementById('stories-container');
    const storyViewerModal = document.getElementById('story-viewer-modal');
    const closeBtn = document.querySelector('.close-story-viewer');
    const storyImage = document.getElementById('story-image');
    const storyVideo = document.getElementById('story-video');
    const storyUserAvatar = document.querySelector('.story-user-avatar');
    const storyUserName = document.querySelector('.story-user-name');
    const prevStoryBtn = document.getElementById('prev-story-btn');
    const nextStoryBtn = document.getElementById('next-story-btn');

    let allStoriesData = [];
    let currentUserStories = [];
    let currentStoryIndex = 0;

    // Fetch stories from the API
    fetch('/api/stories')
        .then(response => response.json())
        .then(data => {
            allStoriesData = data;
            renderStoryCircles(data);
        })
        .catch(error => console.error('Error fetching stories:', error));

    // Render the story circles on the home page
    function renderStoryCircles(data) {
        data.forEach(user => {
            const storyCircle = document.createElement('div');
            storyCircle.classList.add('story', 'text-center');
            storyCircle.dataset.userId = user.user_id;
            storyCircle.innerHTML = `
                <div class="story-circle">
                    <img src="${user.user_avatar}" alt="${user.user_full_name}'s Story" class="rounded-circle">
                </div>
                <div class="username text-muted small">${user.user_full_name}</div>
            `;
            storiesContainer.appendChild(storyCircle);
        });
    }

    // Open the story viewer when a story circle is clicked
    storiesContainer.addEventListener('click', function(event) {
        const storyCircle = event.target.closest('.story');
        if (storyCircle && storyCircle.dataset.userId) {
            const userId = parseInt(storyCircle.dataset.userId, 10);
            const userData = allStoriesData.find(u => u.user_id === userId);
            if (userData && userData.stories.length > 0) {
                currentUserStories = userData.stories;
                currentStoryIndex = 0;
                openStoryViewer(userData); // Pass the whole user object
            }
        }
    });

    function openStoryViewer(userData) {
        if (!userData || currentUserStories.length === 0) return;

        const story = currentUserStories[currentStoryIndex];

        storyUserName.textContent = userData.user_full_name;
        storyUserAvatar.src = userData.user_avatar;

        if (story.media_type === 'image') {
            storyImage.src = story.file_path;
            storyImage.style.display = 'block';
            storyVideo.style.display = 'none';
        } else if (story.media_type === 'video') {
            storyVideo.src = story.file_path;
            storyVideo.style.display = 'block';
            storyImage.style.display = 'none';
            storyVideo.play();
        }

        storyViewerModal.style.display = 'block';
        updateNavButtons();
    }

    function closeStoryViewer() {
        storyViewerModal.style.display = 'none';
        storyVideo.pause();
    }

    function showNextStory() {
        if (currentStoryIndex < currentUserStories.length - 1) {
            currentStoryIndex++;
            openStoryViewer();
        } else {
            closeStoryViewer();
        }
    }

    function showPrevStory() {
        if (currentStoryIndex > 0) {
            currentStoryIndex--;
            openStoryViewer();
        }
    }

    function updateNavButtons() {
        prevStoryBtn.style.display = currentStoryIndex > 0 ? 'block' : 'none';
        nextStoryBtn.style.display = currentStoryIndex < currentUserStories.length - 1 ? 'block' : 'none';
    }

    // Event Listeners
    closeBtn.addEventListener('click', closeStoryViewer);
    nextStoryBtn.addEventListener('click', showNextStory);
    prevStoryBtn.addEventListener('click', showPrevStory);
    storyVideo.addEventListener('ended', showNextStory);
});

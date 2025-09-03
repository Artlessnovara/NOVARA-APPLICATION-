document.addEventListener('DOMContentLoaded', function() {

    // Main event listener for the whole body
    document.body.addEventListener('click', function(event) {
        // --- LIKE BUTTON LOGIC ---
        if (event.target.closest('.like-btn')) {
            event.preventDefault();
            const button = event.target.closest('.like-btn');
            const postId = button.dataset.postId;
            const url = `/like/${postId}`;

            fetch(url, { method: 'POST' })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    const postCard = button.closest('.post-card');
                    postCard.querySelector('.like-count').textContent = data.likes_count;
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

        // --- COMMENT BUTTON LOGIC ---
        if (event.target.closest('.comment-btn')) {
            event.preventDefault();
            const button = event.target.closest('.comment-btn');
            const postId = button.dataset.postId;
            const commentsSection = document.getElementById(`comments-section-${postId}`);

            const isVisible = commentsSection.style.display === 'block';
            commentsSection.style.display = isVisible ? 'none' : 'block';

            // Load comments only if the section is now visible and hasn't been loaded before
            if (!isVisible && !commentsSection.dataset.loaded) {
                loadComments(postId);
            }
        }
    });

    // --- COMMENT FORM SUBMISSION ---
    document.body.addEventListener('submit', function(event) {
        if (event.target.matches('.comment-form')) {
            event.preventDefault();
            const form = event.target;
            const postId = form.dataset.postId;
            const textInput = form.querySelector('input[name="text_content"]');
            const textContent = textInput.value.trim();

            if (!textContent) {
                return; // Don't submit empty comments
            }

            fetch(`/comment/${postId}`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ text_content: textContent })
            })
            .then(response => response.json())
            .then(data => {
                if (data.id) {
                    // Add comment to the list
                    const commentList = document.getElementById(`comment-list-${postId}`);
                    const newComment = document.createElement('div');
                    newComment.classList.add('comment');
                    newComment.innerHTML = `<strong>${data.author.full_name}</strong>: ${data.text_content}`;
                    commentList.appendChild(newComment);

                    // Clear the input
                    textInput.value = '';

                    // Update the comment count
                    const postCard = form.closest('.post-card');
                    const countSpan = postCard.querySelector('.comment-count');
                    const currentCount = parseInt(countSpan.textContent, 10);
                    countSpan.textContent = currentCount + 1;
                } else {
                    console.error('Error adding comment:', data.error);
                }
            })
            .catch(error => console.error('Error:', error));
        }
    });

    // --- FUNCTION TO LOAD COMMENTS ---
    function loadComments(postId) {
        const commentsSection = document.getElementById(`comments-section-${postId}`);
        const commentList = document.getElementById(`comment-list-${postId}`);

        fetch(`/comments/${postId}`)
        .then(response => response.json())
        .then(data => {
            commentList.innerHTML = ''; // Clear previous comments
            data.forEach(comment => {
                const commentEl = document.createElement('div');
                commentEl.classList.add('comment');
                commentEl.innerHTML = `<strong>${comment.author.full_name}</strong>: ${comment.text_content}`;
                commentList.appendChild(commentEl);
            });
            commentsSection.dataset.loaded = 'true'; // Mark as loaded
        })
        .catch(error => console.error('Error loading comments:', error));
    }
});

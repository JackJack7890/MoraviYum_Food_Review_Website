const review_panel = document.getElementById('review_panel');
const welcome_panel = document.getElementById('welcome_panel');

setTimeout(function() {
    // Hide the welcome panel
    document.getElementById('welcome_panel').style.display = 'none';
    // Show the review panel
    document.getElementById('review_panel').style.display = 'block';
}, 3000);  // 3000 milliseconds = 3 seconds


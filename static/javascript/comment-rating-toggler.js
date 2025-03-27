document.addEventListener("DOMContentLoaded", function () {
    const ratingsSection = document.getElementById("ratings-contain");
    const commentsSection = document.getElementById("comment-section-container");
    const toggleRatingsBtn = document.getElementById("toggle-ratings");
    const toggleCommentsBtn = document.getElementById("toggle-comments");

    function activateButton(activeButton, inactiveButton) {
        activeButton.style.backgroundColor = "white";  // Active color (Dark blue)
        activeButton.style.color = "black";
        inactiveButton.style.backgroundColor = "#2d8078";   // Inactive color (Gray)
        inactiveButton.style.color = "white";
    }

    toggleRatingsBtn.addEventListener("click", function () {
        ratingsSection.style.display = "block";
        commentsSection.style.display = "none";
        ratingsSection.style.backgroundColor = "white";
        commentsSection.style.backgroundColor = "teal";

        activateButton(toggleRatingsBtn, toggleCommentsBtn);
    });

    toggleCommentsBtn.addEventListener("click", function () {
        ratingsSection.style.display = "none";
        commentsSection.style.display = "block";
        ratingsSection.style.backgroundColor = "teal";
        commentsSection.style.backgroundColor = "white";

        activateButton(toggleCommentsBtn, toggleRatingsBtn);
    });

    // Set default active button
    activateButton(toggleCommentsBtn, toggleRatingsBtn);
    ratingsSection.style.display = "none";
    commentsSection.style.display = "block";
});

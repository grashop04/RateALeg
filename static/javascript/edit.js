document.addEventListener("DOMContentLoaded", function () {
    const bio = document.getElementById("bio");
    const edit_button = document.getElementById("edit-button");
    const done_button = document.getElementById("done-button");
    const profile_pic = document.getElementById("profile-pic");
    const profile_pic_upload = document.getElementById("profile-pic-upload");

    function getCSRFToken() {
        const csrfElement = document.getElementById("csrf_token");
        return csrfElement ? csrfElement.value : "";
    }

    if (edit_button && done_button && bio) {  
        edit_button.addEventListener("click", function () {
            done_button.style.display = "block";
            profile_pic_upload.style.display = "block";
            bio.contentEditable = true;
        });

        done_button.addEventListener("click", function () {
            if (bio) {
                bio.contentEditable = false;
                this.style.display = "none";
                profile_pic_upload.style.display = "none";

                fetch(window.location.href, {  
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                        "X-CSRFToken": getCSRFToken(),
                    },
                    body: JSON.stringify({ bio: bio.innerText })
                })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        alert("Bio updated successfully!");
                        window.location.href = window.location.href;
                    } else {
                        alert("Error updating bio.");
                    }
                })
                .catch(error => {
                    console.error("Error during fetch:", error);
                    alert("An error occurred while updating bio.");
                });
            }
        });
    }

    if (profile_pic_upload && profile_pic) {  
        profile_pic_upload.addEventListener("change", function () {
            if (this.files && this.files[0]) {
                const reader = new FileReader();
                reader.onload = function (e) {
                    profile_pic.src = e.target.result;
                };
                reader.readAsDataURL(this.files[0]);

                const formData = new FormData();
                formData.append("profile_pic", this.files[0]);

                fetch(window.location.href, {  
                    method: "POST",
                    headers: {
                        "X-CSRFToken": getCSRFToken(),
                    },
                    body: formData
                })
                // .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        alert("Profile picture updated successfully!");
                        
                        // Redirect to the profile page after updating profile picture
                        window.location.href = window.location.href;  // Reload the page
                    } else {
                        alert("Error updating profile picture.");
                    }
                })
                .catch(error => {
                    console.error("Error during fetch:", error);
                    alert("An error occurred while updating profile picture.");
                });
            }
        });
    }
});

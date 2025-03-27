document.addEventListener("DOMContentLoaded", function () {
    // get everything
    const bio = document.getElementById("bio");
    const edit_button = document.getElementById("edit-button");
    const done_button = document.getElementById("done-button");
    const profile_pic = document.getElementById("profile-pic");
    const profile_pic_upload = document.getElementById("profile-pic-upload");

    // get CSRF token for security
    function getCSRFToken() {
        const csrfElement = document.getElementById("csrf_token");
        return csrfElement ? csrfElement.value : "";
    }

    // if everything exists
    if (edit_button && done_button && bio) {  
        edit_button.addEventListener("click", function () {
            done_button.style.display = "block";
            profile_pic_upload.style.display = "block";
            bio.contentEditable = true; // make bio editable
        });

        done_button.addEventListener("click", function () {
            if (bio) {
                bio.contentEditable = false; // when done button clicked, make bio not editable
                this.style.display = "none"; // hide done button
                profile_pic_upload.style.display = "none"; // hide profile pic upload

                fetch(window.location.href, { // send bio to server
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                        "X-CSRFToken": getCSRFToken(),
                    },
                    body: JSON.stringify({ bio: bio.innerText }) // bio sent as JSON data
                })
                .then(response => response.json())
            }
        });
    }

    if (profile_pic_upload && profile_pic) {  
        profile_pic_upload.addEventListener("change", function () {
            if (this.files && this.files[0]) {
                const reader = new FileReader(); // reads file
                reader.onload = function (e) { // uploads file
                    profile_pic.src = e.target.result;
                };
                reader.readAsDataURL(this.files[0]);

                const formData = new FormData(); // form to send file to server
                formData.append("profile_pic", this.files[0]);

                fetch(window.location.href, {  
                    method: "POST",
                    headers: {
                        "X-CSRFToken": getCSRFToken(),
                    },
                    body: formData // send form data as body
                })
                .then(response => response.json())
            }
        });
    }
});

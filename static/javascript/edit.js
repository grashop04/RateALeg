document.addEventListener("DOMContentLoaded", function() {
    const bio = document.getElementById("bio");
    const edit_button = document.getElementById("edit-button");
    const end_button = document.getElementById("done-button");
    const profilePic = document.getElementById("profile-pic");
    const profilePicUpload = document.getElementById("profile-pic-upload");

    edit_button.addEventListener("click", function() {
        end_button.style.display = "block";
        bio.contentEditable = true;
    });

    end_button.addEventListener("click", function() {
        paragraph.contentEditable = false;
        this.style.display = "none";
    });

    profilePicUpload.addEventListener("change", function () {
        if (this.files && this.files[0]) {
            const reader = new FileReader();
            reader.onload = function (e) {
                profilePic.src = e.target.result;
            };
            reader.readAsDataURL(this.files[0]);
        }
    });
});

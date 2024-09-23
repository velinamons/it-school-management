document.addEventListener("DOMContentLoaded", function() {
    const experienceOptions = document.querySelectorAll(".experience-option");

    // Handle experience options for visual feedback
    experienceOptions.forEach(option => {
        option.addEventListener("click", function() {
            experienceOptions.forEach(opt => opt.classList.remove("selected"));
            this.classList.add("selected");
        });
    });
});
document.addEventListener("DOMContentLoaded", function () {
    const experienceOptions = document.querySelectorAll(".experience-option");

    // Handle experience options for visual feedback
    experienceOptions.forEach(option => {
        option.addEventListener("click", function () {
            experienceOptions.forEach(opt => opt.classList.remove("selected"));
            this.classList.add("selected");
        });
    });
});

document.addEventListener('DOMContentLoaded', function () {
        const phoneInput = document.querySelector('#id_phone');

        phoneInput.addEventListener('input', function (e) {
            let digits = phoneInput.value.replace(/\D/g, ''); // Only digits

            // Limit to 10 digits (Ukrainian phone number length)
            if (digits.length > 10) digits = digits.substring(0, 10);

            // Format (XXX) XXX-XX-XX as user types
            phoneInput.value = digits.length > 0 ?
                `(${digits.substring(0, 3)}` +
                (digits.length >= 4 ? `) ${digits.substring(3, 6)}` : '') +
                (digits.length >= 7 ? `-${digits.substring(6, 8)}` : '') +
                (digits.length >= 9 ? `-${digits.substring(8, 10)}` : '') : '';
        });

        phoneInput.addEventListener('keydown', function (e) {
            // Allow deletion even when at non-digit positions
            if (e.key === 'Backspace' && phoneInput.value.match(/\D$/)) {
                phoneInput.value = phoneInput.value.slice(0, -1);
            }
        });
    });
// 1. Grab all the elements from the HTML using their IDs
const passwordInput = document.getElementById('password-input');
const strengthLevelText = document.getElementById('strength-level');
const reqLength = document.getElementById('req-length');
const reqUpper = document.getElementById('req-upper');
const reqLower = document.getElementById('req-lower');
const reqNumber = document.getElementById('req-number');
const reqSymbol = document.getElementById('req-symbol');
const generateBtn = document.getElementById('generate-btn');
const suggestedPasswordText = document.getElementById('suggested-password');

// 2. Listen for every single keystroke the user types
passwordInput.addEventListener('input', function() {
    // Get the current text inside the input box
    const password = passwordInput.value; 
    
    // Send it to our rules engine
    evaluatePassword(password); 
});

// 3. The Rules Engine (Regex and Scoring)
function evaluatePassword(password) {
    let score = 0; // Start with a score of 0

    // Rule A: Check Length (At least 8 characters)
    if (password.length >= 8) {
        reqLength.classList.add('valid'); // Turns it green via CSS
        reqLength.innerText = '✓ At least 8 characters';
        score += 1;
    } else {
        reqLength.classList.remove('valid'); // Turns it back to red
        reqLength.innerText = '✗ At least 8 characters';
    }

    // Rule B: Check Uppercase Letters
    // /[A-Z]/ looks for ANY uppercase letter from A to Z
    if (/[A-Z]/.test(password)) {
        reqUpper.classList.add('valid');
        reqUpper.innerText = '✓ Contains uppercase letter';
        score += 1;
    } else {
        reqUpper.classList.remove('valid');
        reqUpper.innerText = '✗ Contains uppercase letter';
    }

    // Rule C: Check Lowercase Letters
    if (/[a-z]/.test(password)) {
        reqLower.classList.add('valid');
        reqLower.innerText = '✓ Contains lowercase letter';
        score += 1;
    } else {
        reqLower.classList.remove('valid');
        reqLower.innerText = '✗ Contains lowercase letter';
    }

    // Rule D: Check Numbers
    if (/[0-9]/.test(password)) {
        reqNumber.classList.add('valid');
        reqNumber.innerText = '✓ Contains number';
        score += 1;
    } else {
        reqNumber.classList.remove('valid');
        reqNumber.innerText = '✗ Contains number';
    }

    // Rule E: Check Special Symbols
    if (/[!@#$%^&*(),.?":{}|<>]/.test(password)) {
        reqSymbol.classList.add('valid');
        reqSymbol.innerText = '✓ Contains special symbol';
        score += 1;
    } else {
        reqSymbol.classList.remove('valid');
        reqSymbol.innerText = '✗ Contains special symbol';
    }

    // 4. Update the visual Strength Meter based on the final score
    updateStrengthMeter(score, password.length);
}

// 5. Function to update the text and color of the strength meter
function updateStrengthMeter(score, length) {
    if (length === 0) {
        strengthLevelText.innerText = 'None';
        strengthLevelText.style.color = 'black';
    } else if (score <= 2) {
        strengthLevelText.innerText = 'Weak';
        strengthLevelText.style.color = '#d9534f'; // Red
    } else if (score === 3 || score === 4) {
        strengthLevelText.innerText = 'Medium';
        strengthLevelText.style.color = '#f0ad4e'; // Orange
    } else if (score === 5 && length >= 12) {
        // Bonus for having all character types AND being long
        strengthLevelText.innerText = 'Very Strong';
        strengthLevelText.style.color = '#5cb85c'; // Green
    } else if (score === 5) {
        strengthLevelText.innerText = 'Strong';
        strengthLevelText.style.color = '#5cb85c'; // Green
    }
}

// 6. The Password Generator
generateBtn.addEventListener('click', function() {
    // A pool of all possible characters
    const chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()_+~`|}{[]:;?><,./-=";
    let generatedPassword = "";
    const length = 16; // We want a secure 16-character password

    // Loop 16 times, grabbing a random character from the pool each time
    for (let i = 0; i < length; i++) {
        const randomIndex = Math.floor(Math.random() * chars.length);
        generatedPassword += chars[randomIndex];
    }

    // Display it to the user
    suggestedPasswordText.innerText = "Suggested Alternative: " + generatedPassword;
});
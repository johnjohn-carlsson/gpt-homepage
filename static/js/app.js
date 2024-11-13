// Handle disturbance and demo video playback logic
const disturbanceVideo = document.getElementById('disturbance-video');
const avatarVideo = document.getElementById('avatar-video');

// Hardcoded video paths
const idleVideoUrl = '/static/videos/WIN_20240927_19_23_19_Pro.mp4';  // Idle video path
const demoVideoUrl = '/static/videos/test_video.mp4';  // Demo video path

let playDisturbanceInterval;  // Declare disturbance interval globally

// Initially hide the disturbance video
disturbanceVideo.style.display = 'none';

// Function to show disturbance effect
function playDisturbance(callback) {
    disturbanceVideo.style.display = 'block';  // Show the disturbance video
    disturbanceVideo.play();  // Play the short disturbance video

    // Hide disturbance video after it finishes (assuming 0.5 seconds duration)
    setTimeout(() => {
        disturbanceVideo.style.display = 'none';  // Hide the video after it plays

        if (callback) callback();  // Execute callback if provided (e.g., switching to another video)
    }, 500);  // Adjust this time if your disturbance video has a different duration
}

// Function to continuously play disturbance video every 10 seconds
function startDisturbanceLoop() {
    playDisturbance();  // Play disturbance immediately on page load
    playDisturbanceInterval = setInterval(playDisturbance, 10000);  // Play disturbance every 10 seconds
}

// Function to switch to demo videos (with sound enabled)
function playDemoVideo() {
    // Clear the response box and print a message
    const message = 'Find out more here: [https://john-john.nu/about]';
    typeResponseTextWithSpeech(message, null, 50);  // No audio for this message

    // Play disturbance effect before switching to first demo video
    playDisturbance(() => {
        // Switch to first demo video (test_video.mp4)
        avatarVideo.src = demoVideoUrl;  // Set source to the first demo video
        avatarVideo.muted = false;  // Unmute demo video to enable sound
        avatarVideo.loop = false;  // Ensure demo video doesn't loop
        avatarVideo.play();

        // When the first demo video ends, play the second demo video
        avatarVideo.onended = function() {
            // Play disturbance before switching to the second demo video
            playDisturbance(() => {
                // Switch to the second demo video (test_video_2.mp4)
                const secondDemoVideoUrl = '/static/videos/test_video_2.mp4';  // Second demo video path
                avatarVideo.src = secondDemoVideoUrl;
                avatarVideo.play();

                // When the second demo video ends, switch back to the idle video
                avatarVideo.onended = function() {
                    // Play disturbance again after the second demo ends
                    playDisturbance(() => {
                        // Switch back to idle video after disturbance
                        avatarVideo.src = idleVideoUrl;
                        avatarVideo.loop = true;  // Idle video should loop
                        avatarVideo.muted = true;  // Mute the idle video
                        avatarVideo.play();
                    });
                };
            });
        };
    });
}

// Start disturbance effect loop on page load
window.onload = function() {
    startDisturbanceLoop();  // Start disturbance loop when the page loads
};

// Function to handle both typing effect and speech playback
function typeResponseTextWithSpeech(responseText, audioUrl, speed = 70) {
    const responseDiv = document.getElementById('avatar-response');
    responseDiv.innerHTML = '';  // Clear previous content

    // Split the responseText into an array of text and link objects
    const parsedResponse = parseResponseText(responseText);

    let currentPart = 0;
    let currentCharIndex = 0;

    // Function to type out each part character by character
    function typeNextCharacter() {
        if (currentPart < parsedResponse.length) {
            const part = parsedResponse[currentPart];

            if (part.type === 'text') {
                // Type out each character for plain text
                if (currentCharIndex < part.content.length) {
                    responseDiv.innerHTML += part.content.charAt(currentCharIndex);
                    currentCharIndex++;
                    setTimeout(typeNextCharacter, speed);  // Continue typing text
                } else {
                    // Move to next part once text part is fully typed
                    currentPart++;
                    currentCharIndex = 0;
                    setTimeout(typeNextCharacter, speed);
                }
            } else if (part.type === 'link') {
                // Create and append an anchor element for the link
                if (currentCharIndex === 0) {
                    const link = document.createElement('a');
                    link.href = part.url;
                    link.target = '_blank';
                    link.textContent = part.displayText; // Display the link text
                    link.style.color = '#0000EE';  // Optional: link color
                    link.style.textDecoration = 'underline';  // Optional: underline
                    responseDiv.appendChild(link);
                    currentCharIndex++;  // This makes sure we don't repeat link creation
                }
                
                // After displaying the link, move to the next part
                currentPart++;
                currentCharIndex = 0;
                setTimeout(typeNextCharacter, speed);
            }

            // Scroll to the bottom of the responseDiv
            responseDiv.scrollTop = responseDiv.scrollHeight;
        }
    }

    // Start typing effect
    typeNextCharacter();

    // Play the audio if provided
    if (audioUrl) {
        const audio = new Audio(audioUrl);
        audio.play();
    }
}

// Function to parse the responseText and extract links
function parseResponseText(responseText) {
    const regex = /\[(https?:\/\/[^\s\]]+)\]/g;
    let match;
    let lastIndex = 0;
    const parts = [];

    while ((match = regex.exec(responseText)) !== null) {
        // Add text before the link
        if (match.index > lastIndex) {
            parts.push({
                type: 'text',
                content: responseText.substring(lastIndex, match.index)
            });
        }

        // Add the link
        parts.push({
            type: 'link',
            url: match[1],
            displayText: match[1]  // You can modify this to show a different display text
        });

        lastIndex = regex.lastIndex;
    }

    // Add any remaining text after the last link
    if (lastIndex < responseText.length) {
        parts.push({
            type: 'text',
            content: responseText.substring(lastIndex)
        });
    }

    return parts;
}

// Function to submit form and handle response
function submitForm() {
    let userInput = document.getElementById('user-input').value.trim().toLowerCase();

    // Clear the input field after submission
    document.getElementById('user-input').value = '';  // Clear input box

    // Check if the user input contains the word "demo"
    if (userInput.includes('demo')) {
        // Play the demo video sequence
        playDemoVideo();
    } else {
        // Send the request to the Flask server for other inputs
        fetch('/get_response', {
            method: 'POST',
            headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
            body: new URLSearchParams({ 'user_input': userInput })
        })
        .then(response => response.json())
        .then(data => {
            if (data.response && data.audio_url) {
                typeResponseTextWithSpeech(data.response, data.audio_url, 50);
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });
    }
}


// Event listeners for form submission
document.getElementById('input-form').addEventListener('submit', function (e) {
    e.preventDefault();  // Prevent page reload on form submission
    submitForm();  // Trigger form submission
});

document.getElementById('user-input').addEventListener('keydown', function (e) {
    if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();  // Prevent a new line from being added
        submitForm();  // Trigger form submission
    }
});

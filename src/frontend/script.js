// Connect to WebSocket
const ws = new WebSocket("ws://127.0.0.1:8000/ws/");

ws.addEventListener('open', () => {
    console.log('Connected to the WebSocket');
});

// Listen for new media
ws.addEventListener('message', event => {
    const data = JSON.parse(event.data);
    console.log(data)
    if (data.action === 'new_media') {
        displayMedia(data.media_url, data.message);
    }
});

// Display new media
function displayMedia(mediaUrl, message) {
    const mediaContainer = document.getElementById('media-container');

    // Clear previous media
    mediaContainer.innerHTML = '';

    // Create a div to hold the media and message
    const mediaWrapper = document.createElement('div');
    console.log(message)


    // Display the message
    if (message) {
        const messageElement = document.createElement('p');
        messageElement.innerText = message;
        mediaWrapper.appendChild(messageElement);
    }

    const isImage = /\.(jpg|jpeg|png|gif)$/i.test(mediaUrl);
    const isVideo = /\.(mp4|webm|ogg)$/i.test(mediaUrl);
    const isAudio = /\.(mp3|wav|ogg)$/i.test(mediaUrl);
    let mediaElement;

    if (isImage) {
        mediaElement = document.createElement('img');
        mediaElement.src = mediaUrl;
        
        // Remove the image after 10 seconds
        setTimeout(() => {
            mediaWrapper.innerHTML = '';
            mediaContainer.innerHTML = '';

        }, 10000);
    } else if (isVideo) {
        mediaElement = document.createElement('video');
        mediaElement.src = mediaUrl;
        mediaElement.autoplay = true;
        
        // Remove the video when it ends
        mediaElement.addEventListener('ended', () => {
            mediaWrapper.innerHTML = '';
            mediaContainer.innerHTML = '';

        });
    } else if (isAudio) {
        mediaElement = document.createElement('audio');
        mediaElement.src = mediaUrl;
        mediaElement.autoplay = true;
        
        // Remove the audio when it ends
        mediaElement.addEventListener('ended', () => {
            mediaWrapper.innerHTML = '';
            mediaContainer.innerHTML = '';
        });
    }

    // Append the media element to the wrapper
    mediaWrapper.appendChild(mediaElement);

    // Append the wrapper to the container
    mediaContainer.appendChild(mediaWrapper);
}

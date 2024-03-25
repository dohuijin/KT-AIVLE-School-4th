function playPause(musicId) {
    const audioPlayer = document.querySelector(`.music-container[data-audio="${musicId}"] .custom-audio`);
    if (audioPlayer.paused) {
        audioPlayer.play();
    } else {
        audioPlayer.pause();
    }
}

function stopAudio(musicId) {
    const audioPlayer = document.querySelector(`.music-container[data-audio="${musicId}"] .custom-audio`);
    audioPlayer.pause();
    audioPlayer.currentTime = 0;
}

function setVolume(musicId) {
    const audioPlayer = document.querySelector(`.music-container[data-audio="${musicId}"] .custom-audio`);
    audioPlayer.volume = document.getElementById(`volume-${musicId}`).value;
}

function updateProgressBar(musicId) {
    const audioPlayer = document.querySelector(`.music-container[data-audio="${musicId}"] .custom-audio`);
    const progressBar = document.getElementById(`progress-bar-${musicId}`);
    const timeDisplay = document.getElementById(`time-display-${musicId}`);

    const percentage = (audioPlayer.currentTime / audioPlayer.duration) * 100;
    progressBar.style.width = `${percentage}%`;
    timeDisplay.textContent = `${formatTime(audioPlayer.currentTime)} / ${formatTime(audioPlayer.duration)}`;
}

function seek(event, musicId) {
    const audioPlayer = document.querySelector(`.music-container[data-audio="${musicId}"] .custom-audio`);
    const progressBar = document.getElementById(`progress-bar-${musicId}`);

    const rect = progressBar.getBoundingClientRect();
    const totalWidth = rect.width;
    const clickX = event.clientX - rect.left;
    const percentage = (clickX / totalWidth);
    audioPlayer.currentTime = percentage * audioPlayer.duration;
    updateProgressBar(musicId);
}

function downloadAudio(musicId) {
    const audioPlayer = document.querySelector(`.music-container[data-audio="${musicId}"] .custom-audio`);
    const downloadLink = document.createElement('a');
    downloadLink.href = audioPlayer.src;
    downloadLink.download = 'audio.mp3';
    document.body.appendChild(downloadLink);
    downloadLink.click();
    document.body.removeChild(downloadLink);
}

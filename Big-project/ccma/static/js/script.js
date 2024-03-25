const audioPlayer = document.getElementById('custom-audio');
const progressBar = document.getElementById('progress-bar');
const timeDisplay = document.getElementById('time-display');

function playPause() {
    if (audioPlayer.paused) {
        audioPlayer.play();
    } else {
        audioPlayer.pause();
    }
}

function stopAudio() {
    audioPlayer.pause();
    audioPlayer.currentTime = 0;
}

function setVolume() {
    audioPlayer.volume = document.getElementById('volume').value;
}

function formatTime(seconds) {
    const minutes = Math.floor(seconds / 60);
    const remainingSeconds = Math.floor(seconds % 60);
    return `${minutes}:${remainingSeconds < 10 ? '0' : ''}${remainingSeconds}`;
}

function updateProgressBar() {
    const percentage = (audioPlayer.currentTime / audioPlayer.duration) * 100;
    progressBar.style.width = `${percentage}%`;
    timeDisplay.textContent = `${formatTime(audioPlayer.currentTime)} / ${formatTime(audioPlayer.duration)}`;
}

// 오디오 재생 시간을 감지하여 프로그래스 바 갱신
audioPlayer.addEventListener('timeupdate', updateProgressBar);

// 프로그래스 바 클릭 시 해당 위치로 이동
function seek(event) {
    const rect = progressBar.getBoundingClientRect();
    const totalWidth = rect.width;
    const clickX = event.clientX - rect.left;
    const percentage = (clickX / totalWidth);
    audioPlayer.currentTime = percentage * audioPlayer.duration;
    updateProgressBar(); // 클릭한 위치로 이동 후 프로그래스 바 업데이트
}

progressBar.addEventListener('click', seek);

//음악 다운로드
function downloadAudio() {
    const downloadLink = document.createElement('a');
    downloadLink.href = audioPlayer.src;
    downloadLink.download = 'audio.mp3';
    document.body.appendChild(downloadLink);
    downloadLink.click();
    document.body.removeChild(downloadLink);
}
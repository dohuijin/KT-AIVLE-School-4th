document.addEventListener("DOMContentLoaded", () => {

  
  const video = document.getElementById("video");
  video.addEventListener('loadedmetadata', function() {
    // 비디오가 로드되면 이벤트가 발생
    video.controls = true;
  });
  const play = document.getElementById("play");
  const stop = document.getElementById("stop");
  const progress = document.getElementById("progress");
  const timestamp = document.getElementById("timestamp");

  //재생 or 일시정지 and 아이콘 업데이트

  function playOrPauseVideo() {
    if (video.paused) {
      video.play();
      play.innerHTML = `<i class="fa fa-pause fa-2x"></i>`;
    } else {
      video.pause();
      play.innerHTML = `<i class="fa fa-play fa-2x"></i>`;
    }
  }

  // 비디오 멈추기 버튼

  function stopVideo() {
    video.currentTime = 0;
    video.pause();
    play.innerHTML = `<i class="fa fa-play fa-2x"></i>`;
  }

  // input range 변경하기

  function updateProgress() {
    progress.value = (video.currentTime / video.duration) * 100;   



    let min = Math.floor(video.currentTime / 60);
    let sec = Math.floor(video.currentTime % 60);
    if( min < 10){
        min = '0' + String(min);
    }
    if( sec < 10){
        sec = '0' + String(sec);
    }

    timestamp.innerText = min + ':' + sec;
  }

  // progress 바 움직이면 비디오 화면 변경 되기

  function updateTime(){
    console.log(video.currentTime)
    video.currentTime = (progress.value * video.duration) / 100;
    
  }

  video.addEventListener("click", playOrPauseVideo);
  video.addEventListener("timeupdate", updateProgress);
  play.addEventListener("click", playOrPauseVideo);
  stop.addEventListener("click", stopVideo);
  progress.addEventListener('input', updateTime);
});

function capture() {
    const video = document.getElementById("video");
    const canvas = document.createElement("canvas");
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    canvas.getContext("2d").drawImage(video, 0, 0, canvas.width, canvas.height);
    const dataURL = canvas.toDataURL("image/png");
    
    const a = document.createElement("a");
    a.href = dataURL;
    a.download = "capture.png";
    const image = document.getElementById("input");
    const formData = new FormData();
    const blob = dataURItoBlob(dataURL);
    const video_url = document.getElementById("video").src;
    var set_time = +document.getElementById("set_time").value;
    var music_type = document.getElementById("music_type").value;
    var minus_sound = +document.getElementById("minus_sound").value;
   
    if ( minus_sound > 30 ){
        minus_sound =  30;
    }
    else if ( minus_sound < 10 ){
      minus_sound = 10;
    }

    formData.append('image', blob, 'capture.png');
    formData.append('video_url',video_url)
    formData.append('set_time',set_time)
    formData.append('start_time',video.currentTime)
    formData.append('music_type',music_type);
  
    formData.append('minus_sound',minus_sound);


    const csrftoken = getCookie('csrftoken');

    // CSRF 토큰을 헤더에 추가
    /*
    const headers = new Headers({
        'X-CSRFToken': csrftoken
    });
    fetch('/video/result/', {
        method: 'POST',
        body: formData,
        headers: headers,
    })
    .then(response => response.json())
    .then(data => {
        const audioElement = document.getElementById("test");
        audioElement.src = data.video_url;
        audioElement.load();
    })
    .catch(error => {
        console.error('Error:', error);
    });
    */
    $.ajax({
      url: '/video/result/',
      type: 'POST',
      data: formData,
      dataType: 'json',
      contentType: false,
      processData: false,
      headers: {
          'X-CSRFToken': csrftoken,
      },
      beforeSend: function() {
          $('.letter').css('display','inline');
      },
      complete: function() {
          $(".letter").hide();
          $("#audio-container").show();
      },
      success: function(data) {
        console.log(data)
        const audioElement = document.getElementById("test");
        audioElement.src = data.video_url;
        audioElement.load();
      },
      error: function(error) {
          console.error('Error:', error);
      }
  });
  
}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function dataURItoBlob(dataURI) {
    const byteString = atob(dataURI.split(',')[1]);
    const mimeString = dataURI.split(',')[0].split(':')[1].split(';')[0];
    const arrayBuffer = new ArrayBuffer(byteString.length);
    const uint8Array = new Uint8Array(arrayBuffer);

    for (let i = 0; i < byteString.length; i++) {
        uint8Array[i] = byteString.charCodeAt(i);
    }

    return new Blob([arrayBuffer], { type: mimeString });
}
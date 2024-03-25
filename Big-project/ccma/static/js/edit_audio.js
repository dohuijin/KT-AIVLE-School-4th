function capture() {
    const image = document.getElementById("image").src;
    const formData = new FormData();
    var set_time = +document.getElementById("set_time").value;
    var music_type = document.getElementById("music_type").value;
    var minus_sound = +document.getElementById("minus_sound").value;
    formData.append('image', image);
    formData.append('set_time',set_time);
    formData.append('music_type',music_type);
    formData.append('minus_sound',minus_sound);
    const csrftoken = getCookie('csrftoken');
    $.ajax({
        url: '/main/result/',
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
            const audioElement = document.getElementById("custom-audio");
            const downaudioElement = document.getElementById("download_audio");
            audioElement.src = "/media/" + data.audio_url;
            downaudioElement.href = "/media/" + data.audio_url;
            document.getElementById('custom-audio').play();
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

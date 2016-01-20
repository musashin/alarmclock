
/*
Refresh the current play state:
    - Play/Stop button state
    - Currently played track
*/
function refresh_play_state(){

    $.get( "/play_state", function( data ) {

        console.log(data.play)
        if(data.play)
        {
            $('#music-play').prop('disabled', true);
            $('#music-stop').prop('disabled', false);
        }
        else
        {
            $('#music-play').prop('disabled', false);
            $('#music-stop').prop('disabled', true);
        }
    });

}

/*
Request to play a track
*/
function play_track(track_name)
{
    $.post("/play_request",{nothing: false},
    function(){
        alert("playing");
    })
}
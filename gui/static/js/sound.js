
var refresh_delay_ms = 2000
/*
Refresh the current play state:
    - Play/Stop button state
    - Currently played track
*/
function refresh_play_state(){

    $.get( "/play_state", function( data ) {

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
    $.post("/play_request",{track: track_name},
    function(){
        setTimeout(function(){ refresh_play_state();}, refresh_delay_ms);
    })
}

/*
Request to stop current track
*/
function stop_track()
{
    $.post("/stop_request",{},
    function(){
        setTimeout(function(){ refresh_play_state();}, refresh_delay_ms);
    })
}
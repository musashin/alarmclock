

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


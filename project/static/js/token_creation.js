
$( document ).ready(function() {
    $( "#mode-actions-dots" ).click(function() {
        console.log("asdhasdjsa")
        $(".more-action-div").toggle();
    });
    $( "#create-token" ).click(function() {
        sendRequest('POST')
    });
    $( "#refresh-token" ).click(function() {
        sendRequest('PUT')
    });
    $( "#delete-token" ).click(function() {
        sendRequest('DELETE')
    });
    function sendRequest(verb) {
        $("#loading-arrow").show();
        axios({
            method: verb,
            url: '/openid/api/token/',
            responseType: 'json',
            xsrfHeaderName: "X-CSRFToken",
          })
            .then(function (response) {
                console.log(verb)
                data = response.data
                if (verb == 'DELETE') {    
                    $("#token-div-info").hide();
                    $("#create-token").show();
                    $("#token-value").html("");
                    $("#token-last-modified").html("");
                } else {
                    $("#token-div-info").show();
                    $("#create-token").hide();
                    $("#token-value").html( data.token );
                    $("#token-last-modified").html( "Last modified: 0 minutes ago" );
                }
                $("#loading-arrow").hide();
            })
            .catch(function (error) {
                console.log(JSON.stringify(error))
                $("#loading-arrow").hide();
            });
    };
});
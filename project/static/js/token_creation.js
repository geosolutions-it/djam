
$( document ).ready(function() {
    $( "#create-token" ).click(function() {
        sendRequest('POST', null)
    });
    $( "#refresh-token" ).click(function() {
        sendRequest('PUT', null)
    });
    $( "#delete-token" ).click(function() {
        sendRequest('DELETE', null)
    });
    let tokenclipboard = new ClipboardJS('#copy-token');
    tokenclipboard.on('success', function(e) {
        $('#copy-token-result').addClass("shown");
        setTimeout(function(){
            $('#copy-token-result').removeClass("shown");
        },2000);
    });
    let tokenclipboard_wms = new ClipboardJS('#copy-token_wms');
    tokenclipboard_wms.on('success', function(e) {
        $('#copy-token-result_wms').addClass("shown");
        setTimeout(function(){
            $('#copy-token-result_wms').removeClass("shown");
        },2000);
    });
});

function sendRequest(verb, account_id) {
    $("#loading-arrow").show();
    var url = '/openid/api/token/'
    if (account_id != null) {
        url = url + "?account_id=" + account_id
    }
    var arrow_id = "loading-arrow"
    if (account_id != null){
        arrow_id = arrow_id + "-" + account_id
    }
    $("#" + arrow_id).show();

    axios({
        method: verb,
        url: url,
        responseType: 'json',
        xsrfHeaderName: "X-CSRFToken",
      })
        .then(function (response) {

            data = response.data
            
            // deciding the IDs
            var token_value_id = "token-value"
            if (account_id != null){
                token_value_id = token_value_id + "-" + account_id
            }
            var token_div_info = "token-div-info"
            if (account_id != null){
                token_div_info = token_div_info + "-" + account_id
            }
            var token_container_value = "create-token-container"
            if (account_id != null){
                token_container_value = token_container_value + "-" + account_id
            }
            var token_value_id = "token-value"
            if (account_id != null){
                token_value_id = token_value_id + "-" + account_id
            }

            if (verb == 'PATCH') {
                
                var admin_revoke = "admin-revoke"
                if (account_id != null){
                    admin_revoke = admin_revoke + "-" + account_id
                }

                if (data.token == 'Api has been revoked') {
                    $("#" + admin_revoke).text(" Re-enable");
                } else {
                    $("#" + admin_revoke).text(" Revoke");
                }
                $("#" + token_value_id).html(data.token);
                $("#wms-token-value").html( data.wms_token )
            } else if (verb == 'DELETE') {
                $("#" + token_div_info).hide();
                $("#" + token_container_value).show();
                $("#" + token_value_id).html("").hide();
                $("#wms-token-value").html("").hide();
                $("#token-last-modified").html("");
            } else {
                $("#" + token_div_info).show();
                $("#" + token_container_value).hide();
                $("#" + token_value_id).html( data.token ).show();
                $("#wms-token-value").html( data.wms_token ).show();
                $("#token-last-modified").html( "Last modified: 0 minutes ago" );
            }
            $("#" + arrow_id).hide();
        })
        .catch(function (error) {
            console.log(JSON.stringify(error))
            $("#loading-arrow").hide();
        });
}
function colorForDP(color){
    $("#profilePicBox").css("background-color", color);
    $("#overlayPicBox").css("background-color", color);
    $(".overlayPicOptionBox").css("background-color", color);
}

//DP
$("#DPOverlayX").click(function(){
    $("#DPOverlay").css("display", "none");
});
$("#overlayButtonCancel").click(function(){
    $("#DPOverlay").css("display", "none");
});
function CHANGECOLOR(){
    color = $("#inputChangeColor").val();
    $("#overlayPicBox").css("background-color", color);
    $(".overlayPicOptionBox").css("background-color", color);
    checkDPColor();
}
    //Update DP and color to firebase
function updateDP(){
    filePath = $("#overlayPic").attr("src");
    color = $("#inputChangeColor").val();
    $.getJSON("/updateDP", {filePath: filePath, color: color}, function(){
        location.reload();
        }
    )
}

//First Box
    //Display "Save" and "Cancel" button
function focusIn(num){
    $("#profile"+num).focus();
    $("#Edit"+num).css("display", "none");
    $("#Save"+num).css("display", "inline");
    $("#Cancel"+num).css("display", "inline");
}

    //Set cursor position at the end if press "Edit" button
$(".editButton").click(function(){
    var theId = this.getAttribute("id");
    var num = theId[theId.length - 1];
    $("#profile"+num)[0].setSelectionRange(-1, -1);
});

    //Find input that are focus out and call focusOut()
$(".profileInput").focusout(function(){
    var theId = this.getAttribute("id");
    var num = theId[theId.length - 1];
    focusOut(num);
});

//Second Box
    //Make "Update Password" pressable
function activateButton(){
    $("#profileChangePasswordButton").attr("disabled", true);
    $("#profileChangePasswordButton").attr("class", "buttonDisabled");

    $("#errorMessage").css("display", "none");

    if ($("#currPass").val() == "" && $("#newPass").val() == "" && $("#conNewPass").val() == ""){}else{
        if ($("#newPass").val() == $("#conNewPass").val()) {
            if ($("#newPass").val() == $("#currPass").val()) {
                $("#errorMessage").html("<span class='glyphicon glyphicon-exclamation-sign'></span>&nbsp;New password must not be the same as current password.");
                $("#errorMessage").css("display", "block");
            } else {
                if ($("#currPass").val() != "" && $("#newPass").val() != "" && $("#conNewPass").val() != "") {
                    $("#profileChangePasswordButton").attr("disabled", false);
                    $("#profileChangePasswordButton").attr("class", "buttonAbled");
                }
            }
        } else {
            $("#errorMessage").html("<span class='glyphicon glyphicon-exclamation-sign'></span>&nbsp;Passwords do not match.");
            $("#errorMessage").css("display", "block");
        }
    }
}

//Third Box + Modals
    //Change modal content depends on which button pressed
$("#closeAccModalButton").click(function(){
    $("#modalInput").val("");
    $("#modalTopText").text("Close Account");
    $("#modalMiddleText").text("Closing your account is irreversible. Enter your iDiet password to confirm you want to permanently close this account:");
    $("#modalButton").attr("value", "Close Account").attr("name", "closeacc").attr("onclick", "");

});
$("#Save3").mousedown(function(){
    $("#loader3").css("display", "inline-block");
    var newUsername = $("#profile3").val();
    $.getJSON("/checkForSameUsername", {checkThis: newUsername}, function(result){
        if(result == true){
            $("#Save3").trigger("click");
            $("#modalInput").val("");
            $("#modalTopText").text("Update Username");
            $("#modalMiddleText").html("To update your username to (<span id='NewUsername'>"+newUsername+"</span>), enter your current password:");
            $("#modalButton").attr("value", "Update Username").attr("name", "changeusername").attr("onclick", "updateProfile(3)");
        }else if(result == false){
            alert("Same Username already existed.");
            $("#loader3").css("display", "none");
        }
    });
});

function closeModal(){
    $("#DeModal").modal("toggle");
}
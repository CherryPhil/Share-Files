function CHECK(){
    if ($("#passwordNo1").val() != $("#passwordNo2").val()){
        $("#registerErrorMessage").css("display","block");
    }else{
        $("#registerErrorMessage").css("display","none");
    }
}

function CHECK2(){
    if ($("#passwordNo1").val() != $("#passwordNo2").val()){
        $("#registerErrorMessage").css("display","block");
        return false;
    }else{
        $("#registerErrorMessage").css("display","none");
        alert("Register successfully!");
        return true;
    }
}
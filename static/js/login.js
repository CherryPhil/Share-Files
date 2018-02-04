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

//For Admin login
function UserAdminLogin(disBut){
    if(disBut.id == "userButton"){
        $("#adminButton").attr("class", "changeLogin");
        $("#userButton").attr("class", "changeLoginActivate");
        $("#usernameInput").attr("name", "username");
        $("#passwordInput").attr("name", "password").attr("placeholder", "Password");
        $("#loginLogin").attr("name", "login");
    }else if(disBut.id == "adminButton"){
        $("#adminButton").attr("class", "changeLoginActivate");
        $("#userButton").attr("class", "changeLogin");
        $("#usernameInput").attr("name", "adminusername");
        $("#passwordInput").attr("name", "adminpassword").attr("placeholder", "Admin Password");
        $("#loginLogin").attr("name", "adminlogin");
    }
};
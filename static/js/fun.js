var question = [["Maximum carbohydrates are obtained from:", "A"],
                ["Vitamins, minerals and proteins in suitable amounts are given to body by:", "D"],
                ["According to food guide pyramid fats oils and sweets should be used:", "C"],
                ["Sources of proteins includes:", "D"],
                ["A diet containing right amount of energy, carbohydrates, proteins, fats, fiber, vitamins, minerals and water to fulfill requirement of body is called:", "B"]
                ];
var question_choice = [["Whole grain food", "Fatty fish", "Plant oil", "Nuts"],
                        ["Whole grain food", "Fatty fish", "Plant oil", "Nuts"],
                        ["2-3 servings", "Frequently", "Sparingly", "2-4 servings"],
                        ["Fish", "Poultry", "Eggs", "All of them"],
                        ["Nutrition", "Balanced diet", "Perfect diet", "Food pyramid"]
                        ];
var question2 = [["The following are good sources of protein:", "D"],
                ["Why do you need vitamin D:", "C"],
                ["Which is the best carbohydrate choice:", "B"],
                ["Fat is essential to a healthy diet, but not all fats are created equal. Which of the following is a monounsaturated fat, considered to be the healthiest kind of fat for cooking:", "A"],
                ["A protein is called a complete protein when it:", "D"]
                ];
var question_choice2 = [["Milk", "Beans", "Lean beef", "All of the above"],
                        ["To help with digestion", "To help your hair grow", "To help calcium build bones", "So vitamin C won't get lonely"],
                        ["White bread", "Whole-wheat bread", "White rice", "Fruit juice"],
                        ["Olive oil", "Butter", "Coconut oil", "Lard"],
                        ["Is low in fat and high in fiber", "Can be used in place of an egg in a recipe", "Includes white and dark meat", "Contains all essential amino acids, which the body cannot produce on its own"]
                        ];
var question3 = [["What are the Essential Nutrients:", "D"],
                ["Which is NOT one of Galen's 'Laws of Health':", "B"],
                ["What is metabolism determined by:", "D"],
                ["What are Dietary Standards based on:", "D"],
                ["What are the first three things to look for on a food label:", "C"]
                ];
var question_choice3 = [["Carbohydrates, Lipids (fats), and Proteins", "Vitamins and Minerals", "A & B and Water", "A & B, Water and Phytochemicals"],
                        ["Eat the right foods", "Drink 8 glasses of water daily", "Breathe fresh air", "Get enough sleep"],
                        ["Sleep", "Genetics", "Thyroid Gland", "All of the Above"],
                        ["Large groups of people", "Individual diets", "B & C only", "All of the above"],
                        ["1: Fat content, 2: Calorie content, 3: Serving size", "1: Serving size, 2: Servings per container, 3: Carbohydrate content", "1: Fat content, 2: Servings size, 3: Servings per container", "1: Serving size, 2: Fat content, 3: Servings per container"]
                        ];

var challengeScore1 = -1;
var challengeScore2 = -1;
var challengeScore3 = -1;

//Set value from database
function setCha1_2_3(cha1, cha2, cha3){
    challengeScore1 = cha1;
    if(challengeScore1 == 5){$("#OutsideAchieve1").attr("src", "static/images/unAchievement1.png")}
    challengeScore2 = cha2;
    if(challengeScore2 == 5){$("#OutsideAchieve2").attr("src", "static/images/unAchievement2.png")}
    challengeScore3 = cha3;
    if(challengeScore3 == 5){$("#OutsideAchieve3").attr("src", "static/images/unAchievement3.png")}
}


var questions = question;
var question_choices = question_choice;

//3 set of code that replace information in modal box based on different button clicked
//- Set question & multiple choice base on different button clicked
//- Set achievement image
//- Set score text
//- Refresh the question and multiple choice by calling restartFunc()
$("#challengeButton").click(function(){
    questions = question;
    question_choices = question_choice;
    $("#challengeNumber").text("1");
    $("#achievements").attr("src", "static/images/Achievement1.png");
    if(challengeScore1 == -1){
        $("#showScore").text("No previous records")
    }else if(challengeScore1 == -2) {
        $("#showScore").text("Login to store your score!")
    }else{
        $("#showScore").text("Your highest score: "+challengeScore1+"/5");
        if(challengeScore1 == 5){
            $("#achievements").attr("src", "static/images/unAchievement1.png");
        }
    }
    restartFunc();
});
$("#challengeButton2").click(function(){
    questions = question2;
    question_choices = question_choice2;
    $("#challengeNumber").text("2");
    $("#achievements").attr("src", "/static/images/Achievement2.png");
    if(challengeScore2 == -1){
        $("#showScore").text("No previous records")
    }else if(challengeScore2 == -2) {
        $("#showScore").text("Login to store your score!")
    }else{
        $("#showScore").text("Your highest score: "+challengeScore2+"/5");
        if(challengeScore2 == 5){
            $("#achievements").attr("src", "/static/images/unAchievement2.png");
        }
    }
    restartFunc();
});
$("#challengeButton3").click(function(){
    questions = question3;
    question_choices = question_choice3;
    $("#challengeNumber").text("3");
    $("#achievements").attr("src", "static/images/Achievement3.png");
    if(challengeScore3 == -1){
        $("#showScore").text("No previous records")
    }else if(challengeScore3 == -2) {
        $("#showScore").text("Login to store your score!")
    }else{
        $("#showScore").text("Your highest score: "+challengeScore3+"/5");
        if(challengeScore3 == 5){
            $("#achievements").attr("src", "static/images/unAchievement3.png");
        }
    }
    restartFunc();
});


//Restart question shown and multiple choices
var count = 0;
var score = 0;
function restartFunc(){
    score = 0;
    count = 0;
    $("#questionNumber").text(count + 1);
    $("#modalBodyQuestion").text(questions[count][0]);
    $("#C1").text(question_choices[count][0]);
    $("#C2").text(question_choices[count][1]);
    $("#C3").text(question_choices[count][2]);
    $("#C4").text(question_choices[count][3]);
    $("#modalProgress").css("width", "0%");
    $("#modalProgressNo").text(0);
    $("#modalProgress").attr("aria-valuenow", "0");
    $("#A").prop("checked", false);
    $("#B").prop("checked", false);
    $("#C").prop("checked", false);
    $("#D").prop("checked", false);
    $("#errorMessage").css("display", "none");
    $("#modalBodyNext").text("Next Question");
};

//Validate if user got tick radio button
//Alert text when finish, and accumulate score if correct
//Update score to database by .getJSON
function hi(){
    if($("#A").prop("checked") == false && $("#B").prop("checked") == false && $("#C").prop("checked") == false && $("#D").prop("checked") == false){
        $("#errorMessage").css("display", "block");
    }else{
        if ($("#" + questions[count][1]).prop("checked")) {
        score = score + 1;
    }
    $("#errorMessage").css("display", "none");
    $("#A").prop("checked", false);
    $("#B").prop("checked", false);
    $("#C").prop("checked", false);
    $("#D").prop("checked", false);
    var progress_no = Number($("#modalProgressNo").text()) + 25;
    $("#modalProgress").css("width", progress_no + "%");
    $("#modalProgressNo").text(progress_no);
    $("#modalProgress").attr("aria-valuenow", progress_no);

    if (count == 3) {
        $("#modalBodyNext").text("Finish");
    }
    if (count == 4) {
        alert("Congratulation! You have done the challenge, you got " + score + " question correct!!");
        $.getJSON("/userScoreProcess",
            {userScore: score, Qnum: $("#challengeNumber").text()},
            function(data){
            if($("#challengeNumber").text() == 1){
                if(data == 5){
                    $("#OutsideAchieve1").attr("src", "static/images/unAchievement1.png");
                    if(challengeScore1 != 5){showAchievementAlert("static/images/unAchievement1.png", "POWDER POWER");}
                    challengeScore1 = data;}
            }else if($("#challengeNumber").text() == 2){
                if(data == 5){
                    $("#OutsideAchieve2").attr("src", "static/images/unAchievement2.png");
                    if(challengeScore2 != 5){showAchievementAlert("static/images/unAchievement2.png", "DESERVING DINER");}
                    challengeScore2 = data;}
            }else{
                if(data == 5){
                    $("#OutsideAchieve3").attr("src", "static/images/unAchievement3.png");
                    if(challengeScore3 != 5){showAchievementAlert("static/images/unAchievement3.png", "BEAK BECKONING");}
                    challengeScore3 = data;}
            }});
        $('#challengeModal').modal("toggle");
    }

    count = count + 1;
    $("#questionNumber").text(count + 1);
    $("#modalBodyQuestion").text(questions[count][0]);
    $("#C1").text(question_choices[count][0]);
    $("#C2").text(question_choices[count][1]);
    $("#C3").text(question_choices[count][2]);
    $("#C4").text(question_choices[count][3]);
    }
}


function showAchievementAlert(url, text){
    $("#AlertAchievement").attr("src", url);
    $("#AlertText").text(text);
    $("#UnlockAlertBox").fadeIn("slow");
    setTimeout(function(){$("#UnlockAlertBox").fadeOut("slow");}, 3000);
}
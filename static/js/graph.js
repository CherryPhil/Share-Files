var dps = [] ;
var userBMI;
window.onload = function () {
    //var myFirebaseRef = new Firebase('https://idiet-229a2.firebaseio.com/');
    //var userRef = myFirebaseRef.child('users');
    //var dataRef = userRef.child('-L2dS5bg7s-mRLpV6HPk');
    //var bmi = dataRef.child('bmi');
	hello();


    var chart = new CanvasJS.Chart("chartContainer", {
        animationEnabled: true,
        title: {
            text: "Your BMI Progress"
        },
        axisX: {
            title: "Months",
            titleFontSize: 25
        },
        axisY: {
            title: "B M I",
            titleFontSize: 25,
            includeZero: false
        },
        data: [
            {
                type: "line",
                dataPoints: dps
            }
        ]
    });
    chart.render();

    $("#addDataPoint").click(function () {

        if ($("#newdp").val() === 0) {
            alert("No Input Detected")
        }
        else {
            dps.push({y: parseInt(document.getElementById("newdp").value)});
            localStorage.setItem("data", chart.options.data[0].dataPoints);
            chart.render();
            $.getJSON("/updateToFirebase", {bmis: JSON.stringify(dps)}, function (value) {
                if (value == false) {
                    alert("please login to update to firebase")
                }
            })
        }
    });
};
function followDatabase(list){
	console.log(list);
		dps = list;
	}
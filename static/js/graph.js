window.onload = function () {
	var chart = new CanvasJS.Chart("chartContainer", {
	    animationEnabled:true,
		title: {
			text: "Your BMI Progress"
		},
        axisX:{
		    title:"Months",
			titleFontSize:25
        },
        axisY: {
            title: "B M I",
			titleFontSize:25,
            includeZero: false
        },
		data: [
		{
			type: "line",
			dataPoints: [
				{ y: 10 },
				{ y:  4 },
				{ y: 18 },
				{ y:  8 }
			]
		}
		]
	});
	chart.render();

	$("#addDataPoint").click(function () {

	chart.options.title.text = "Your BMI Progress";
	if ($("#newdp").val() == 0) {
        alert("No Input Detected")
    }
	else {
        chart.options.data[0].dataPoints.push({y: parseInt(document.getElementById("newdp").value)});
        localStorage.setItem("data",chart.options.data[0].dataPoints);
        chart.render();
    }
	});

};


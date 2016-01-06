var sites = ["facebook", "twitter", "instagram", "github", "youtube", "soundcloud"];

// request.onreadystatechange = function(){

// 	};

var request = new XMLHttpRequest();
var username = prompt("enter your username ");
var i = 0;
for( ; i < sites.length ; i++) {
	console.log(i);
	//function invocation
	//var yolo = "https://".concat(sites[i]).concat(".com/").concat("gyanl")
	var yolo = "https://"+sites[i]+".com/"+username;
	console.log(yolo);
	xhr = new XMLHttpRequest();
	xhr.open("HEAD", "http://instagram.com/gyanl" ,true);
	xhr.onreadystatechange=function() {
		alert("HTTP Status Code:"+xhr.status)
	}
	xhr.send(null);  
	

	

}







/*
*to execute paste the following script in the console
*/


var sites = ["facebook", "twitter", "instagram", "github","youtube"];
var username = prompt("enter your username ");


f = "https://"+sites[0]+".com/"+username;
fr = new XMLHttpRequest();
fr.open("HEAD", f ,true);
fr.onreadystatechange=function() {
	console.log("HTTP Status Code: facebook "+ fr.status)
}
fr.send(null);

t = "https://"+sites[1]+".com/"+username;
tr = new XMLHttpRequest();
tr.open("HEAD", f ,true);
tr.onreadystatechange=function() {
	console.log("HTTP Status Code: twitter"+ tr.status)
}
tr.send(null);

i = "https://"+sites[2]+".com/"+username;
ir = new XMLHttpRequest();
ir.open("HEAD", f ,true);
ir.onreadystatechange=function() {
	console.log("HTTP Status Code: instagram"+ ir.status)
}
ir.send(null);
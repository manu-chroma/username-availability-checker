var username = document."input[type=my-form]"
var f = "https://facebook.com/".concat(gyanl)
var t = "https://twitter.com/".concat(gyanl)
var i = "https://instagram.com/".concat(gyanl)
for(var i = 0 ; i < 3 ; i++) {
	
}
function getReq(usr) {
    var req = false;
    if(window.XMLHttpRequest) {
        try {
            req = new XMLHttpRequest();
        } catch(e) {
            req = false;
        }
    } else if(window.ActiveXObject) {
        try {
            req = new ActiveXObject("Microsoft.XMLHTTP");
        } catch(e) {
            req = false;
        }
    }
    if (! req) {
        alert("Your browser does not support XMLHttpRequest.");
    }
    return req;
}

    var req = getReq();

        try {
        req.open("GET", 'f', false);
        req.send(usr);
    } catch (e) {
        success = false;
        error_msg = "Error: " + e;
    }

alert(req.status);
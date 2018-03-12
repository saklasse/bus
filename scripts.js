// sample01/scripts.js

var getArticleInfo;
if ( window.XMLHttpRequest)
{
    getArticleInfo = new XMLHttpRequest();
}
else
{
    getArticleInfo = new ActiveXObject("Microsoft.XMLHTTP");
}


getArticleInfo.onreadystatechange = loadText;
getArticleInfo.open("GET", "cgi-bin/bus.py");
getArticleInfo.send();
function loadText() {
    var text = document.getElementById("textTarget");
    if (getArticleInfo.readyState === 4) {
        if (getArticleInfo.status === 200) {
            text.innerHTML = getArticleInfo.responseText;
            console.log('got response' + getArticleInfo.responseText)
        } else {
            console.log('There was a problem with the request.', getArticleInfo.status);
        }
    }
};

function myAlert() {
    getArticleInfo.onreadystatechange = loadText;
    getArticleInfo.open("GET", "cgi-bin/bus.py");
    getArticleInfo.send();
}

setInterval(myAlert, 60000);

var express = require('express');
var app = express();

app.use(express.json());
app.use(express.urlencoded());

var fs = require('fs');
function wubbify(commentId, commentText, sendRes) {
    fs.writeFile(commentId, commentText, function (err, data) {
        if (err) {
            return console.log(err);
        }
        var exec = require('child_process').exec;
        var child = exec('python ../wubbify/dubstepify.py ' + commentId, function (error, stdout, stderr) {
            if (error != null) {
                console.log(stderr);
                return null;
            }

        var exec2 = require('child_process').exec;
	var child = exec2('python upload.py ' + commentId + '.mp3 "' + commentText + '"', function (error, stdout, stderr) {
		if(error !=null) {
			console.log(stderr);
			return null;
			}
			sendRes(stdout);
		});
	    });
    });
}

app.get('/', function (req, res) {
    var body = "Hello, World";
    res.setHeader('Content-Type', 'text/plain');
    res.setHeader('Content-Length', body.length);
    res.end(body);
});

app.post('/wubML/:commentId', function (req, res) {
    var body = "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n<Response>\n<Play>http://cs4414.cloudapp.net/song/"+req.params.commentId+"</Play>\n</Response>"
    res.setHeader('Content-Type', 'text/xml');
    res.setHeader('Content-Length', body.length);
    res.end(body);
});

app.post('/song/:commentId', function (req, res) {
    var body = fs.readFile(req.params.commentId+".mp3", function (err, data) {
	if (err) throw err;
	//console.log("\n\n"+data);
	//return data;
        //console.log("\n\n"+data);
        res.setHeader('Content-Type', 'audio/mpeg');
        res.setHeader('Content-Length', data.length);
        res.end(data);
	});
});

app.post('/wubbify/:commentId', function (req, res) {
    var commentText = req.body.commentText.substring(0,140);
    var commentId = req.params.commentId;
    console.log(commentId+"\n"+commentText);

    var send = function(wubURL) {
        console.log("\n"+wubURL);
	//    var body = commentId + "\n" + commentText;
        res.setHeader('Content-Type', 'text/plain');
        res.setHeader('Content-Length', wubURL.length);
        res.end(wubURL);
    }
    var wubURL = wubbify(commentId, commentText, send);
});

app.listen(80);
console.log("LISTENING ON PORT 80");

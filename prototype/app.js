const express = require('express')
const {spawn} = require('child_process')
const bodyParser = require('body-parser')
const sqlite3 = require('sqlite3').verbose();
require('dotenv/config')
var DB = require('./db/db_methods');
const { db } = require('./models/orders');

const app = express()
app.set('view engine', 'html');
app.engine('html', require('ejs').renderFile);
app.use(bodyParser.urlencoded({extended:true}));
app.use(bodyParser.json())

const port = process.env.PORT || 5000;
const apiKey = process.env.API_KEY;
const apiPassword = process.env.API_PASSWORD;

	
app.get('/', (req, res) => {
	//add buildpack
	var retrievedData;
	var processedDataArray = []
	// spawn new child process to call the python script
	const python = spawn('python3', [__dirname+'test_script.py']);
	console.log("python: " + python)

	python.stdout.on('data', function (data) {
	 console.log("grabbing data from script ...");
	 retrievedData = data.toString();

	 var dataArray = retrievedData.split(',')

	 //THIS IS A HACK, FIX L8R
	 for (var i = 0; i < dataArray.length; i+=2) {
		 processedDataArray.push([dataArray[i].replace('\r', '').replace('\n', ''), dataArray[i+1]])
	 }

	 DB.writeToDB(processedDataArray)
	 DB.readFromDB()	
	 res.render('./index.html', {data: processedDataArray});
	});
	// in close event we are sure that stream from child process is closed
	// python.on('close', (code) => {
	// 	console.log("running close...")
		
	// 	var dataArray = retrievedData.split(',')

	// 	//THIS IS A HACK, FIX L8R
	// 	for (var i = 0; i < dataArray.length; i+=2) {
	// 		processedDataArray.push([dataArray[i].replace('\r', '').replace('\n', ''), dataArray[i+1]])
	// 	}

	// 	DB.writeToDB(processedDataArray)
	// 	DB.readFromDB()	
	// 	res.render('./index.html', {data: processedDataArray});
	// });

})

app.post('/', (req, res) => {
	console.log(req.body)
});

//START
app.listen(port, () => {
	console.log("listening at port " + port)
	console.log("dirname: " + __dirname)
})

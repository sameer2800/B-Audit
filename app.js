const express = require('express');
const path = require('path');
var bodyParser = require('body-parser');
var request = require('request');
var mysql = require('mysql');
var connection = mysql.createConnection({
  host: '',
  user: '',
  password: '',
  database: ''
})

connection.connect();

const app = express();

var logged = false;

app.set('views', path.join(__dirname, 'views'));
app.set('view engine', 'pug');

app.use(bodyParser.json()); // support json encoded bodies
app.use(bodyParser.urlencoded({ extended: true })); // support encoded bodies

app.get('/', function(req, res){
  res.render('index');
});

app.get('/owner-register', function(req, res){
  res.render('owner_register');
});

app.post('/owner-register', function(req, res){
  res.render('owner_register');
});

app.get('/owner-login', function(req, res){
  res.render('owner_login');
});

app.get('/contractor-register', function(req, res){
  res.render('contractor_register');
});

app.get('/contractor-login', function(req, res){
  res.render('contractor_login');
});

app.get('/owner', function(req, res){
  res.render('owner');
});

app.get('/contractor', function(req, res){
  res.render('contractor');
});

app.get('/marketplace', function(req, res){
  res.render('marketplace');
});

app.listen(3000, function(){
  console.log('Server started on port 3000');
});

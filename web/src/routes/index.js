var express = require('express');
var router = express.Router();
var path = require('path');

/* GET home page. */
router.get('/', function(req, res, next) {
  //res.render('new_index', { title: 'Dean\'s website'});
  res.render('index');
  

});

module.exports = router;

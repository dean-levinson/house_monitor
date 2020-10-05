var express = require('express');
var router = express.Router();
var path = require('path');

/* GET home page. */
router.get('/', function(req, res, next) {
  res.render('new_index', { title: 'Dean\'s website'});
  //res.sendFile(path.join(__dirname, 'new_index.html'));
  

});

module.exports = router;

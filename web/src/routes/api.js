var express = require('express');
var router = express.Router();

router.get('/computers', function(req, res) {
    req.app.locals.db.collection("computers").find({}).toArray(function(err, result) {
        if (err) throw err;
        res.json(result);
    });
});

module.exports = router;
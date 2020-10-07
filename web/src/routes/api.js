var express = require('express');
var router = express.Router();
var amqp = require('amqplib/callback_api')
const computers_data = require('./computers.json');

let computers = []

amqp.connect('amqp://localhost', function(error0, connection) {
    if (error0) {
        console.log("Got ERROR while connecting to RMQ: ", error0);
        return;
    }

    connection.createChannel(function(error1, channel) {
        if (error1) {
            console.log("Got ERROR while creating channel: ", error1)
        }

        var queue = 'computersQueue';

        channel.assertQueue(queue, {
            durable: false
        });

        console.log(" [*] Waiting for messages in %s", queue);

        channel.consume(queue, function(msg) {
            console.log(" [x] Received %s", msg.content.toString());
            computers.push(JSON.parse(msg.content.toString()))
            }, {
            noAck: true
        });
    });
});

router.get('/computers', function(req, res) {
    res.json(computers);
});

module.exports = router;
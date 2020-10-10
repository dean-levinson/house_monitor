const socketIo = require("socket.io");

module.exports.start_io = function(server, app)  {
    const io = socketIo(server);

    let interval;

    const computersCollection = app.locals.db.collection("computers")

    io.on("connection", (socket) => {
        console.log("New client connected");
        // if (interval) {
        //     clearInterval(interval);
        // }
        getApiAndEmit(socket)
        changeStream = computersCollection.watch()
        // interval = setInterval(() => getApiAndEmit(socket), 1000);
        changeStream.on("change", next => {
            console.log("Change detected!", next);
            getApiAndEmit(socket);
        });
        socket.on("disconnect", () => {
            console.log("Client disconnected");
            clearInterval(interval);
        });
    });

    const getApiAndEmit = socket => {
        app.locals.db.collection("computers").find({}).toArray(function(err, result) {
            if (err) throw err;
            // Emitting a new message. Will be consumed by the client
            socket.emit("FromAPI", result);
        });
    };
};

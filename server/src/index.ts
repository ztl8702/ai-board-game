import {ActorFactory} from "./actor";
import { Player } from "./logic";

var cryptolib = require("crypto");

var app = require('express')();
var expressSession = require('express-session');
var sharedSession = require('express-socket.io-session');

app.set('trust proxy', 1) // trust first proxy

var session = expressSession({
    secret: 'mysecret',
    resave: true,
    saveUninitialized: true,
    maxAge: 24 * 60 * 60 * 1000 * 10 // 10 days
});

app.use(session);

var http = require('http').Server(app);

var io = require('socket.io')(http);

app.get('/', function (req, res) {
    res.sendFile(__dirname + '/www/index.html');
    console.log('session', req.session);
    if (req.session.playerId == null) {
        req.session.playerId = cryptolib.randomBytes(16).toString("hex");
    }
})

io.use(sharedSession(session));

io.on('connection', function (socket) {
    let playerId = socket.handshake.session.playerId;
    console.log('a user connected. ',playerId);
    if (playerId != null) {
        let thePlayer : Player = ActorFactory.getActor('Player', playerId);
        thePlayer.setSocket(socket);
        
        // player's client events
        socket.on('joinRoom', function (roomId) {
            thePlayer.tryJoinRoom(roomId);
        });

        socket.on('leaveRoom', function () {
            thePlayer.leaveRoom();
        });

        socket.on('setNickname',function() {

        });
        socket.on('makeMove', function (data) {
            thePlayer.tryTakeAction();
        });

        socket.on('disconnect', function() {
            //do nothing
            // player might reconnect
        })

    }

});

http.listen(3000, function () {
    console.log('listening on port 3000')
})

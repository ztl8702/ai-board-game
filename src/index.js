"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
var actor_1 = require("./actor");
var cryptolib = require("crypto");
var app = require('express')();
var expressSession = require('express-session');
var sharedSession = require('express-socket.io-session');
app.set('trust proxy', 1); // trust first proxy
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
    res.sendFile('index.html', { 'root': './www/' });
    console.log('session', req.session);
    if (req.session.playerId == null) {
        req.session.playerId = cryptolib.randomBytes(16).toString("hex");
    }
});
io.use(sharedSession(session));
io.on('connection', function (socket) {
    var playerId = socket.handshake.session.playerId;
    console.log('a user connected. ', playerId);
    if (playerId != null) {
        var thePlayer_1 = actor_1.ActorFactory.getActor('Player', playerId);
        thePlayer_1.setSocket(socket);
        //@todo: update user-agent, ip, etc.
        // player's client events
        socket.on('playerSyncRequest', function (callback) {
            //thePlayer
            //setImmediate(()=>thePlayer.pushSync());
        });
        socket.on('roomSyncRequest', function (roomId) {
            var theRoom = actor_1.ActorFactory.getActor('GameRoom', roomId);
            var syncObject = theRoom.getSyncObject();
            thePlayer_1.send('roomSync', syncObject);
        });
        socket.on('joinRoom', function (roomId) {
            thePlayer_1.tryJoinRoom(roomId);
        });
        socket.on('leaveRoom', function (callback) {
            thePlayer_1.leaveRoom();
        });
        socket.on('setNickname', function (newNickname) {
            console.log('Player ' + thePlayer_1.nickName + ' changing name to ' + newNickname);
            thePlayer_1.nickName = newNickname;
            // send room update
        });
        socket.on('startGame', function () {
            thePlayer_1.tryStartGame();
        });
        socket.on('makeMove', function (move, callback) {
            try {
                var result = thePlayer_1.tryTakeAction(move);
                callback(result);
            }
            catch (e) {
                console.log(e);
            }
        });
        socket.on('disconnect', function () {
            thePlayer_1.removeSocket();
            //do nothing
            // player might reconnect
        });
    }
});
http.listen(3000, function () {
    console.log('listening on port 3000');
});

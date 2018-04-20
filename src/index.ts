import { ActorFactory } from "./actor";
import { Player, GameRoomState, GameRoom } from "./logic";
import { setImmediate } from "timers";
import { DBConnection } from "./db";
const express = require('express');
var cryptolib = require("crypto");

// DB
var conn = new DBConnection();
ActorFactory._conn = conn;
conn.test().then(_ => {
    conn.migrate();
});


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
    res.sendFile('index.html', { 'root': './public/' });
    //console.log('session', req.session);
    if (req.session.playerId == null) {
        req.session.playerId = cryptolib.randomBytes(16).toString("hex");
    }
})

app.use(express.static('public'));
io.use(sharedSession(session));

io.on('connection', function (socket) {
    let playerId = socket.handshake.session.playerId;
    console.log('a user connected. ', playerId);
    if (playerId != null) {
        let thePlayer: Player = ActorFactory.getActor('Player', playerId);
        thePlayer.setSocket(socket);
        //@todo: update user-agent, ip, etc.

        // player's client events
        socket.on('playerSyncRequest', function (callback) {
            //thePlayer
            setImmediate(() => thePlayer.pushSync());
        });

        socket.on('roomSyncRequest', function (roomId) {
            if (roomId == null) return;
            let theRoom: GameRoom = ActorFactory.getActor('GameRoom', roomId);
            let syncObject = theRoom.getSyncObject();
            thePlayer.send('roomSync', syncObject);
        });

        socket.on('sessionSyncRequest', function (roomId) {
            if (roomId == null) return;
            let theRoom: GameRoom = ActorFactory.getActor('GameRoom', roomId);
            let syncObject = theRoom.getSessionSyncObject();
            thePlayer.send('sessionSync', syncObject);
        });
        socket.on('joinRoom', function (roomId) {
            thePlayer.tryJoinRoom(roomId);
        });

        socket.on('leaveRoom', function (callback) {
            thePlayer.leaveRoom();
        });

        socket.on('setNickname', function (newNickname) {
            console.log('Player ' + thePlayer.nickName + ' changing name to ' + newNickname);
            thePlayer.nickName = newNickname;
            // send room update

        });

        socket.on('startGame', function () {
            thePlayer.tryStartGame();
        });

        socket.on('newSession', function () {
            thePlayer.tryNewSession();
        })

        socket.on('makeMove', function (move, callback) {
            try {
                var result = thePlayer.tryTakeAction(move);
                callback(result);
            } catch (e) {
                console.log(e);
            }

        });

        socket.on('disconnect', function () {
            thePlayer.removeSocket();
            //do nothing
            // player might reconnect
        })

    }

});

http.listen(3000, function () {
    console.log('listening on port 3000')
})

"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
var Board_1 = require("./Board");
var _1 = require("./");
var index_1 = require("../actor/index");
var GameRoom = /** @class */ (function () {
    function GameRoom(id) {
        var _this = this;
        this.playerCount = 0;
        console.log("GameRoom", id, "created.");
        this.id = id;
        this.state = GameRoomState.WaitingForPlayers;
        this.observers = [];
        this.currentSession = this.currentSession = index_1.ActorFactory.getActor("GameSession", null);
        this.currentSession.onPushSync = function () { _this.broadcastSessionSync(); };
    }
    GameRoom.prototype.isFull = function () {
        return this.playerCount >= 2;
    };
    GameRoom.prototype.addPlayer = function (newPlayer) {
        var result = false;
        switch (this.state) {
            case GameRoomState.WaitingForPlayers:
                // black player first
                if (this.playerCount == 0) {
                    this.blackPlayer = newPlayer;
                    ++this.playerCount;
                    result = true;
                    console.log("Player " + newPlayer.nickName + " joined GameRoom " + this.id + " as black player.");
                }
                else if (this.playerCount == 1) {
                    this.whitePlayer = newPlayer;
                    ++this.playerCount;
                    result = true;
                    console.log("Player " + newPlayer.nickName + " joined GameRoom " + this.id + " as white player.");
                }
                if (this.playerCount == 2) {
                    this.changeState(GameRoomState.Ready);
                    this.broadcastRoomSync();
                }
                break;
        }
        return result;
    };
    GameRoom.prototype.removePlayer = function (player) {
        function doRemovePlayer(player) {
            if (player == this.blackPlayer) {
                this.blackPlayer = null;
                this.playerCount--;
            }
            else if (player == this.whitePlayer) {
                this.whitePlayer = null;
                this.playerCount--;
            }
        }
        switch (this.state) {
            case GameRoomState.Playing:
                // the game is ongoing
                doRemovePlayer(player);
                this.changeState(GameRoomState.DisplayResult);
                break;
            case GameRoomState.WaitingForPlayers, GameRoomState.DisplayResult:
                doRemovePlayer(player);
                break;
            case GameRoomState.Ready:
                doRemovePlayer(player);
                this.changeState(GameRoomState.WaitingForPlayers);
                break;
        }
        this.broadcastRoomSync();
    };
    GameRoom.prototype.addObserver = function (obs) {
        if (this.observers.indexOf(obs) == -1) {
            this.observers.push(obs);
        }
        this.broadcastRoomSync();
    };
    GameRoom.prototype.removeObserver = function (obs) {
        var index = this.observers.indexOf(obs);
        if (index != -1) {
            this.observers.splice(index, 1);
        }
        this.broadcastRoomSync();
    };
    GameRoom.prototype.startGame = function () {
        if (this.state == GameRoomState.Ready) {
            this.currentSession.start();
            this.changeState(GameRoomState.Playing);
            this.broadcastRoomSync();
            this.broadcastSessionSync();
        }
    };
    GameRoom.prototype.broadcastRoomSync = function () {
        // Send room sync to all players and observers
        var roomSync = this.getSyncObject();
        function sendRoomSyncToPlayer(p, rs) {
            p.send('roomSync', rs);
        }
        if (this.blackPlayer)
            sendRoomSyncToPlayer(this.blackPlayer, roomSync);
        if (this.whitePlayer)
            sendRoomSyncToPlayer(this.whitePlayer, roomSync);
        this.observers.forEach(function (obs) {
            sendRoomSyncToPlayer(obs, roomSync);
        });
    };
    GameRoom.prototype.broadcastSessionSync = function () {
        var s = this.currentSession.getSyncObject();
        function sendRoomSyncToPlayer(p, rs) {
            p.send('sessionSync', rs);
        }
        if (this.blackPlayer)
            sendRoomSyncToPlayer(this.blackPlayer, s);
        if (this.whitePlayer)
            sendRoomSyncToPlayer(this.whitePlayer, s);
        this.observers.forEach(function (obs) {
            sendRoomSyncToPlayer(obs, s);
        });
    };
    GameRoom.prototype.getLatestResult = function () {
    };
    GameRoom.prototype.newSession = function () {
        var _this = this;
        if (this.state == GameRoomState.DisplayResult || this.state == GameRoomState.Playing) {
            this.currentSession.onPushSync = null;
            this.currentSession.onUpdate = null;
            index_1.ActorFactory.archiveActor("GameSession", this.currentSession.getId());
            this.currentSession = index_1.ActorFactory.getActor("GameSession", null);
            this.currentSession.onPushSync = function () { _this.broadcastSessionSync(); };
            if (this.isFull()) {
                this.changeState(GameRoomState.Ready);
            }
            else {
                this.changeState(GameRoomState.WaitingForPlayers);
            }
        }
    };
    GameRoom.prototype.getSessionSyncObject = function () {
        return this.currentSession.getSyncObject();
    };
    GameRoom.prototype.getSyncObject = function () {
        var result = {
            blackPlayerId: this.blackPlayer ? this.blackPlayer.getId() : null,
            blackPlayerName: this.blackPlayer ? this.blackPlayer.nickName : null,
            whitePlayerId: this.whitePlayer ? this.whitePlayer.getId() : null,
            whitePlayerName: this.whitePlayer ? this.whitePlayer.nickName : null,
            state: this.state,
            observersCount: this.observers.length
        };
        return result;
    };
    GameRoom.prototype.changeState = function (newState) {
        if (newState != this.state) {
            this.state = newState;
            // notify players
        }
    };
    GameRoom.prototype.whichPlayer = function (p) {
        if (p == this.whitePlayer)
            return Board_1.PlayerColor.White;
        if (p == this.blackPlayer)
            return Board_1.PlayerColor.Black;
        return null;
    };
    GameRoom.prototype.tryTakeAction = function (act, caller) {
        if (this.state != GameRoomState.Playing) {
            var result = new _1.PlayerActionResult(false);
            result.message = "Game is not started.";
            return result;
        }
        var side = this.whichPlayer(caller);
        if (side == null) {
            var result = new _1.PlayerActionResult(false);
            result.message = "You are not playing in this room.";
            return result;
        }
        var result = this.currentSession.tryTakeAction(act, side);
        return result;
    };
    return GameRoom;
}());
exports.GameRoom = GameRoom;
var GameRoomState;
(function (GameRoomState) {
    GameRoomState[GameRoomState["WaitingForPlayers"] = 0] = "WaitingForPlayers";
    GameRoomState[GameRoomState["Ready"] = 1] = "Ready";
    GameRoomState[GameRoomState["Playing"] = 2] = "Playing";
    GameRoomState[GameRoomState["DisplayResult"] = 3] = "DisplayResult";
})(GameRoomState = exports.GameRoomState || (exports.GameRoomState = {}));

"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
var index_1 = require("../actor/index");
var faker = require("faker");
var Player = /** @class */ (function () {
    function Player(id) {
        this.id = id;
        this.state = PlayerState.NoRoom;
        this.nickName = faker.name.findName(); // create a random name
        console.log("New Player " + this.nickName + " (" + this.id + "). ");
    }
    Object.defineProperty(Player.prototype, "nickName", {
        get: function () {
            return this._nickName;
        },
        set: function (value) {
            this._nickName = value;
        },
        enumerable: true,
        configurable: true
    });
    Player.prototype.getId = function () {
        return this.id;
    };
    Player.prototype.notifyStart = function () {
        if (this.socketIO) {
            this.socketIO.emit('gameStarted');
        }
    };
    Player.prototype.setSocket = function (socket) {
        this.socketIO = socket;
    };
    Player.prototype.removeSocket = function () {
        this.socketIO = null;
    };
    // actions
    Player.prototype.tryJoinRoom = function (roomId) {
        if (this.state == PlayerState.NoRoom) {
            var room = index_1.ActorFactory.getActor('GameRoom', roomId);
            var result = room.addPlayer(this);
            if (result) {
                this.state = PlayerState.JoinedAsPlayer;
                this.gameRoom = room;
            }
            return result;
        }
        else {
            return false;
        }
    };
    Player.prototype.leaveRoom = function () {
        if (this.state == PlayerState.JoinedAsPlayer) {
            this.gameRoom.removePlayer(this);
            this.gameRoom = null;
            this.state = PlayerState.NoRoom;
        }
        else if (this.state == PlayerState.JoinedAsObserver) {
            this.gameRoom.removeObserver(this);
            this.gameRoom = null;
            this.state = PlayerState.NoRoom;
        }
    };
    Player.prototype.observeRoom = function (roomId) {
        if (this.state == PlayerState.NoRoom) {
            var room = index_1.ActorFactory.getActor('GameRoom', roomId);
            room.addObserver(this);
            this.gameRoom = room;
            this.state = PlayerState.JoinedAsObserver;
        }
    };
    Player.prototype.tryTakeAction = function (a) {
        if (this.state == PlayerState.JoinedAsPlayer) {
            var result = this.gameRoom.tryTakeAction(a, this);
            return result;
        }
        return PlayerActionResult.failed("You are not in a room.");
    };
    Player.prototype.newSession = function () {
    };
    Player.prototype.tryStartGame = function () {
        if (this.state == PlayerState.JoinedAsPlayer) {
            this.gameRoom.startGame();
        }
    };
    Player.prototype.send = function () {
        var args = [];
        for (var _i = 0; _i < arguments.length; _i++) {
            args[_i] = arguments[_i];
        }
        if (this.socketIO != null) {
            (_a = this.socketIO).emit.apply(_a, args);
        }
        var _a;
    };
    return Player;
}());
exports.Player = Player;
var PlayerState;
(function (PlayerState) {
    PlayerState[PlayerState["NoRoom"] = 0] = "NoRoom";
    PlayerState[PlayerState["JoinedAsPlayer"] = 1] = "JoinedAsPlayer";
    PlayerState[PlayerState["JoinedAsObserver"] = 2] = "JoinedAsObserver";
})(PlayerState || (PlayerState = {}));
var PlayerActionType;
(function (PlayerActionType) {
    PlayerActionType[PlayerActionType["Place"] = 0] = "Place";
    PlayerActionType[PlayerActionType["MakeMove"] = 1] = "MakeMove";
})(PlayerActionType = exports.PlayerActionType || (exports.PlayerActionType = {}));
var PlayerAction = /** @class */ (function () {
    function PlayerAction() {
    }
    return PlayerAction;
}());
exports.PlayerAction = PlayerAction;
var PlayerActionResult = /** @class */ (function () {
    function PlayerActionResult(isSuccess) {
        this.isSuccess = isSuccess;
    }
    PlayerActionResult.success = function () {
        return new PlayerActionResult(true);
    };
    PlayerActionResult.failed = function (reason) {
        var result = new PlayerActionResult(false);
        result.message = reason;
        return result;
    };
    return PlayerActionResult;
}());
exports.PlayerActionResult = PlayerActionResult;

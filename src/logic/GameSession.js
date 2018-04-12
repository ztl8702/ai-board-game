"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
var _1 = require("./");
var timers_1 = require("timers");
var GameSession = /** @class */ (function () {
    function GameSession(id) {
        // @todo: double check spec
        this.upperHand = _1.PlayerColor.Black;
        this.NUMBER_OF_PIECES = 12;
        this.round = 0; // counts through both placing and moving phases
        this.board = new _1.Board();
        this.ended = false;
        this.id = id;
        console.log("New GameSession " + id);
    }
    GameSession.prototype.getId = function () {
        return this.id;
    };
    GameSession.prototype.start = function () {
        this.startTime = new Date(Date.now());
        this.round = 0;
        this.moveCount = 0;
        this.actions = [];
        this.nextRound();
    };
    GameSession.prototype.tryTakeAction = function (act, color) {
        var _this = this;
        if (this.ended)
            return _1.PlayerActionResult.failed("Game ended.");
        console.log('color', color);
        if (this.turn != color)
            return _1.PlayerActionResult.failed("Not your turn.");
        var colorStr = (color == _1.PlayerColor.Black) ? _1.Board.CELL_BLACK : _1.Board.CELL_WHITE;
        if (this.phase == GamePhase.Placing && act.type == _1.PlayerActionType.Place) {
            // handling placing
            var a = act;
            if (!this.board.canPlace(a.newX, a.newY, colorStr)) {
                return _1.PlayerActionResult.failed("Cannot place pieces here.");
            }
            this.board.placeNewPiece(a.newX, a.newY, colorStr);
            if (color == _1.PlayerColor.Black) {
                --this.blackToPlace;
            }
            else {
                --this.whiteToPlace;
            }
            this.actions.push([this.round, color, act]);
            timers_1.setImmediate(function () { return _this.nextRound(); });
            timers_1.setImmediate(function () { return _this.sendUpdate({
                lastMove: _this.actions[_this.actions.length - 1],
                timeSinceStart: _this.getTime(),
                phase: _this.phase,
                timeLeftForThisTurn: -1
            }); });
            return _1.PlayerActionResult.success();
        }
        else if (this.phase == GamePhase.Moving && act.type == _1.PlayerActionType.MakeMove) {
            // handling moving
            var a = act;
            var fromP = [a.fromX, a.fromY];
            var toP = [a.toX, a.toY];
            if (!(this.board.get(a.fromX, a.fromY) == colorStr && this.board.isValidMove(fromP, toP))) {
                return _1.PlayerActionResult.failed("Invalid move. Try again.");
            }
            this.board.makeMove(fromP, toP);
            this.actions.push([this.round, color, act]);
            this.moveCount++;
            timers_1.setImmediate(function () { return _this.nextRound(); });
            return _1.PlayerActionResult.success();
        }
        else {
            return _1.PlayerActionResult.failed("Invalid action type.");
        }
    };
    GameSession.prototype.nextRound = function () {
        var _this = this;
        if (this.ended)
            return;
        //DEBUG
        console.log("Round " + this.round);
        this.board.printBoard();
        console.log("");
        console.log("");
        if (this.round == 0) {
            // initialise
            this.round = 1;
            this.turn = this.upperHand;
            this.phase = GamePhase.Placing;
            this.whiteToPlace = this.NUMBER_OF_PIECES;
            this.blackToPlace = this.NUMBER_OF_PIECES;
        }
        // @todo: check winning first
        if (this.phase == GamePhase.Moving) {
            if (this.moveCount == 128 || this.moveCount == 192) {
                // after move #128 and #192
                this.board.shrinkBoard();
                // @todo: check winning again
                timers_1.setImmediate(function () { return _this.pushSync(); });
            }
            this.round++;
            this.roundStartTime = new Date(Date.now());
        }
        else if (this.phase == GamePhase.Placing) {
            if (this.whiteToPlace == 0 && this.blackToPlace == 0) {
                // placing phase ended
                this.phase = GamePhase.Moving;
                this.turn = this.upperHand;
                this.roundStartTime = new Date(Date.now());
                timers_1.setImmediate(function () { return _this.pushSync(); });
            }
            else {
                this.turn = (this.turn == _1.PlayerColor.Black) ? _1.PlayerColor.White : _1.PlayerColor.Black;
            }
            this.round++;
        }
    };
    GameSession.prototype.getTime = function () {
        // seconds since the start of the game
        var now = new Date(Date.now());
        return (now.getTime() - this.startTime.getTime()) / 1000;
    };
    GameSession.prototype.getSyncObject = function () {
        return {
            board: this.board.getMatrix(),
            round: this.round,
            turn: this.turn,
            winner: this.board.getWinner(),
            phase: this.phase,
            listOfMoves: this.actions,
            timeSinceStart: this.getTime(),
            timeLeftForThisTurn: -1
        };
    };
    GameSession.prototype.sendUpdate = function (u) {
        if (this.onUpdate) {
            this.onUpdate(u); // what to send?
        }
    };
    GameSession.prototype.pushSync = function () {
        if (this.onPushSync) {
            var s = this.getSyncObject();
            this.onPushSync(s);
        }
    };
    return GameSession;
}());
exports.GameSession = GameSession;
var GamePhase;
(function (GamePhase) {
    GamePhase[GamePhase["Placing"] = 0] = "Placing";
    GamePhase[GamePhase["Moving"] = 1] = "Moving";
})(GamePhase = exports.GamePhase || (exports.GamePhase = {}));

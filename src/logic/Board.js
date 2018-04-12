"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
var Board = /** @class */ (function () {
    function Board() {
        this.BOARD_MAX_SIZE = 8;
        this.DIRECTION = [
            [-1, 0],
            [+1, 0],
            [0, -1],
            [0, +1] // down
        ];
        // initialise the board
        this.board = [];
        for (var i = 0; i < this.BOARD_MAX_SIZE; ++i) {
            var row = [];
            for (var j = 0; j < this.BOARD_MAX_SIZE; ++j) {
                row.push(Board.CELL_EMPTY);
            }
            this.board.push(row);
        }
        // current board size
        this.currentBoardSize = 8;
        this.updateCorners();
    }
    Board.prototype.getCorners = function () {
        return [
            [this.minX, this.minY],
            [this.minX, this.maxY],
            [this.maxX, this.minY],
            [this.maxX, this.maxY]
        ];
    };
    Board.prototype.updateCorners = function () {
        var _this = this;
        // set the corners
        this.getCorners().forEach(function (pos) {
            _this.set(pos[0], pos[1], Board.CELL_CORNER);
        });
    };
    Board.prototype.set = function (x, y, value) {
        if (!this.isWithinBoard(x, y)) {
            throw "(" + x + "," + y + ") is not in board";
        }
        this.board[x][y] = value;
    };
    Board.prototype.get = function (x, y) {
        if (!this.isWithinBoard(x, y)) {
            return Board.CELL_DEAD;
        }
        else {
            return this.board[x][y];
        }
    };
    Object.defineProperty(Board.prototype, "minX", {
        get: function () {
            return this.BOARD_MAX_SIZE - this.currentBoardSize;
        },
        enumerable: true,
        configurable: true
    });
    Object.defineProperty(Board.prototype, "maxX", {
        get: function () {
            return this.minX + this.currentBoardSize - 1;
        },
        enumerable: true,
        configurable: true
    });
    Object.defineProperty(Board.prototype, "minY", {
        get: function () {
            return this.minX;
        },
        enumerable: true,
        configurable: true
    });
    Object.defineProperty(Board.prototype, "maxY", {
        get: function () {
            return this.maxX;
        },
        enumerable: true,
        configurable: true
    });
    Board.prototype.isWithinBoard = function (x, y) {
        return (Number.isInteger(x) && Number.isInteger(y)) && (this.minX <= x && x <= this.maxX && this.minY <= y && y <= this.maxY);
    };
    Board.prototype.getWinner = function () {
        if (this.checkWinning(PlayerColor.Black)) {
            return PlayerColor.Black;
        }
        else if (this.checkWinning(PlayerColor.White)) {
            return PlayerColor.White;
        }
        else {
            return null;
        }
    };
    Board.prototype.checkWinning = function (color) {
        var colorStr = color == PlayerColor.Black ? Board.CELL_BLACK : Board.CELL_WHITE;
        var opponentColor = this.getOpponentColor(colorStr);
        var myCount = 0;
        var opponentCount = 0;
        for (var x = this.minX; x <= this.maxX; ++x) {
            for (var y = this.minY; y <= this.maxY; ++y) {
                if (this.get(x, y) == colorStr) {
                    ++myCount;
                }
                else if (this.get(x, y) == opponentColor) {
                    ++opponentCount;
                }
            }
        }
        // we win if we have pieces left but the opponent does not
        return (myCount > 0 && opponentCount == 0);
    };
    Board.prototype.getOpponentColor = function (myColor) {
        if (myColor == Board.CELL_BLACK) {
            return Board.CELL_WHITE;
        }
        else {
            return Board.CELL_BLACK;
        }
    };
    Board.prototype.printBoard = function () {
        // for debug purposes
        for (var i = 0; i < this.BOARD_MAX_SIZE; ++i) {
            var row = '';
            for (var j = 0; j < this.BOARD_MAX_SIZE; ++j) {
                row += this.get(j, i) + ' ';
            }
            console.log(row);
        }
    };
    Board.prototype.makeMove = function (fromPos, toPos) {
        var ourColor = this.get(fromPos[0], fromPos[1]);
        var opponentColor = this.getOpponentColor(ourColor);
        this.set(fromPos[0], fromPos[1], Board.CELL_EMPTY);
        this.set(toPos[0], toPos[1], ourColor);
        this.doElimination(toPos[0], toPos[1]);
    };
    Board.prototype.placeNewPiece = function (x, y, color) {
        if (color !== Board.CELL_BLACK && color !== Board.CELL_WHITE) {
            throw "Invalid color";
        }
        if (!this.isWithinBoard(x, y)) {
            throw "Invalid position";
        }
        if (this.get(x, y) != Board.CELL_EMPTY) {
            throw "Cell not empty";
        }
        this.set(x, y, color);
        this.doElimination(x, y);
    };
    Board.prototype.doElimination = function (newX, newY) {
        var _this = this;
        var ourColor = this.get(newX, newY);
        var opponentColor = this.getOpponentColor(ourColor);
        // step 1: our piece eliminating opponent
        this.DIRECTION.forEach(function (direction) {
            var adjPieceX = newX + direction[0];
            var adjPieceY = newY + direction[1];
            var adjPiece2X = adjPieceX + direction[0];
            var adjPiece2Y = adjPieceY + direction[1];
            if (_this.isWithinBoard(adjPieceX, adjPieceY) &&
                _this.get(adjPieceX, adjPieceY) == opponentColor &&
                _this.isWithinBoard(adjPiece2X, adjPiece2Y) &&
                [ourColor, Board.CELL_CORNER].indexOf(_this.get(adjPiece2X, adjPiece2Y)) != -1) {
                _this.set(adjPieceX, adjPieceY, Board.CELL_EMPTY);
            }
        });
        // step 2: opponent eliminating ours
        if (this.isWithinBoard(newX - 1, newY) && [opponentColor, Board.CELL_CORNER].indexOf(this.get(newX - 1, newY)) != -1
            && this.isWithinBoard(newX + 1, newY) && [opponentColor, Board.CELL_CORNER].indexOf(this.get(newX + 1, newY)) != -1) {
            this.set(newX, newY, Board.CELL_EMPTY);
        }
        if (this.isWithinBoard(newX, newY - 1) && [opponentColor, Board.CELL_CORNER].indexOf(this.get(newX, newY - 1)) != -1
            && this.isWithinBoard(newX, newY + 1) && [opponentColor, Board.CELL_CORNER].indexOf(this.get(newX, newY + 1)) != -1) {
            this.set(newX, newY, Board.CELL_EMPTY);
        }
    };
    Board.prototype.getMatrix = function () {
        return this.board;
    };
    Board.prototype.shrinkBoard = function () {
        var _this = this;
        if (this.currentBoardSize <= 4)
            return;
        // clean the circle
        for (var i = this.minX; i <= this.maxX; ++i) {
            this.set(i, this.minY, Board.CELL_DEAD);
            this.set(i, this.maxY, Board.CELL_DEAD);
        }
        for (var i = this.minY + 1; i <= this.maxY - 1; ++i) {
            this.set(this.minX, i, Board.CELL_DEAD);
            this.set(this.maxX, i, Board.CELL_DEAD);
        }
        this.currentBoardSize -= 2;
        this.updateCorners();
        // do the elimination
        this.getCorners().forEach(function (pos) {
            var x = pos[0];
            var y = pos[1];
            _this.DIRECTION.forEach(function (direction) {
                var adjPieceX = x + direction[0];
                var adjPieceY = y + direction[1];
                var adjPiece2X = adjPieceX + direction[0];
                var adjPiece2Y = adjPieceY + direction[1];
                if (_this.isWithinBoard(adjPieceX, adjPieceY) &&
                    _this.get(adjPieceX, adjPieceY) in [Board.CELL_BLACK, Board.CELL_WHITE] &&
                    _this.isWithinBoard(adjPiece2X, adjPiece2Y) &&
                    _this.get(adjPiece2X, adjPiece2Y) in [Board.CELL_BLACK, Board.CELL_WHITE]) {
                    if (_this.get(adjPieceX, adjPieceY) != _this.get(adjPiece2X, adjPiece2Y)) {
                        _this.set(adjPieceX, adjPieceY, Board.CELL_EMPTY);
                    }
                }
            });
        });
    };
    Board.prototype.isValidMove = function (fromPos, toPos) {
        function mean(a, b) {
            return (a + b) / 2;
        }
        return (this.isWithinBoard(fromPos[0], fromPos[1]) && this.isWithinBoard(toPos[0], toPos[1])
            && ([Board.CELL_BLACK, Board.CELL_WHITE].indexOf(this.get(fromPos[0], fromPos[1])) != -1)
            && (this.get(toPos[0], toPos[1]) == Board.CELL_EMPTY)
            && ((Math.abs(toPos[0] - fromPos[0]) + Math.abs(toPos[1] - fromPos[1]) == 1) // adjacent
                || (Math.abs(toPos[0] - fromPos[0]) + Math.abs(toPos[1] - fromPos[1]) == 2 // two steps away
                    && Math.abs(toPos[0] - fromPos[0]) * Math.abs(toPos[1] - fromPos[1]) == 0 // not diagonal
                    && this.get(fromPos[0], fromPos[1]) == this.get(mean(fromPos[0], toPos[0]), mean(fromPos[1], toPos[1]))) // adj == adj2
            ));
    };
    Board.prototype.canPlace = function (x, y, color) {
        if (!(this.isWithinBoard(x, y) && this.get(x, y) == Board.CELL_EMPTY)) {
            return false;
        }
        if (color == Board.CELL_WHITE && y <= 5)
            return true;
        if (color == Board.CELL_BLACK && y >= 2)
            return true;
        return false;
    };
    Board.CELL_EMPTY = ' ';
    Board.CELL_BLACK = 'B';
    Board.CELL_WHITE = 'W';
    Board.CELL_CORNER = 'X';
    Board.CELL_DEAD = 'D';
    return Board;
}());
exports.Board = Board;
var PlayerColor;
(function (PlayerColor) {
    PlayerColor[PlayerColor["Black"] = 0] = "Black";
    PlayerColor[PlayerColor["White"] = 1] = "White";
})(PlayerColor = exports.PlayerColor || (exports.PlayerColor = {}));

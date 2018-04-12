export class Board {
    private readonly BOARD_MAX_SIZE: number = 8;
    private readonly CELL_EMPTY: string = ' ';
    private readonly CELL_BLACK: string = 'B';
    private readonly CELL_WHITE: string = 'W';
    private readonly CELL_CORNER: string = 'X';
    private readonly CELL_DEAD: string = 'D';

    private board: Array<Array<string>>;
    private currentBoardSize: number;

    private readonly DIRECTION = [
        [-1, 0],  // left
        [+1, 0],  // right
        [0, -1],  // up
        [0, +1]   // down
    ];

    constructor() {
        // initialise the board
        this.board = []
        for (let i = 0; i < this.BOARD_MAX_SIZE; ++i) {
            let row = [];
            for (let j = 0; j < this.BOARD_MAX_SIZE; ++j) {
                row.push(this.CELL_EMPTY);
            }
            this.board.push(row);
        }


        // current board size
        this.currentBoardSize = 8;
        this.updateCorners();
    }

    private updateCorners() {
        // set the corners

        this.set(0, 0, this.CELL_CORNER);
        this.set(0, this.currentBoardSize - 1, this.CELL_CORNER);
        this.set(this.currentBoardSize - 1, 0, this.CELL_CORNER);
        this.set(this.currentBoardSize - 1, this.currentBoardSize - 1, this.CELL_CORNER);
    }

    public set(x, y, value) {
        if (!this.isWithinBoard(x, y)) {
            throw "Not in board";
        }
        this.board[x][y] = value;
    }

    public get(x, y): string {
        if (!this.isWithinBoard(x, y)) {
            return this.CELL_DEAD;
        } else {
            return this.board[x][y];
        }
    }

    private get minX(): number {
        return this.BOARD_MAX_SIZE - this.currentBoardSize;
    }

    private get maxX(): number {
        return this.minX + this.currentBoardSize - 1;
    }

    private get minY(): number {
        return this.minX;
    }

    private get maxY(): number {
        return this.maxX;
    }

    public isWithinBoard(x, y): boolean {
        return (this.minX <= x && x <= this.maxX && this.minY <= y && y <= this.maxY);
    }



    private checkWinning(color: PlayerColor) {
        let colorStr = color == PlayerColor.Black ? this.CELL_BLACK : this.CELL_WHITE;
        let opponentColor = this.getOpponentColor(colorStr);

        let myCount = 0;
        let opponentCount = 0;
        for (let x = this.minX; x <= this.maxX; ++x) {
            for (let y = this.minY; y <= this.maxY; ++y) {
                if (this.get(x, y) == colorStr) {
                    ++myCount;
                } else if (this.get(x, y) == opponentColor) {
                    ++opponentCount;
                }
            }
        }
        // we win if we have pieces left but the opponent does not
        return (myCount > 0 && opponentCount == 0);
    }

    private getOpponentColor(myColor: string): string {
        if (myColor == this.CELL_BLACK) {
            return this.CELL_WHITE;
        } else {
            return this.CELL_BLACK;
        }
    }


    public printBoard(): void {
        // for debug purposes
        for (var i = 0; i < this.BOARD_MAX_SIZE - 1; ++i) {
            let row = '';
            for (var j = 1; j < this.BOARD_MAX_SIZE - 1; ++j) {
                row += this.get(j, i) + ' '
            }
            console.log(row);
        }
    }

    public makeMove(fromPos: [number, number], toPos: [number, number]): void {
        var ourColor = this.get(fromPos[0], fromPos[1]);
        var opponentColor = this.getOpponentColor(ourColor);
        this.set(fromPos[0], fromPos[1], this.CELL_EMPTY);
        this.set(toPos[0], toPos[1], ourColor);
        this.doElimination(toPos[0], toPos[1]);
    }

    public placeNewPiece(x, y, color) {
        if (color !== this.CELL_BLACK && color !== this.CELL_WHITE) {
            throw "Invalid color";
        }
        if (!this.isWithinBoard(x, y)) {
            throw "Invalid position";
        }
        if (this.get(x, y) != this.CELL_EMPTY) {
            throw "Cell not empty";
        }
        this.set(x, y, color);
        this.doElimination(x,y);
    }

    private doElimination(newX: number, newY: number) {
        let ourColor = this.get(newX, newY);
        let opponentColor = this.getOpponentColor(ourColor);
        // step 1: our piece eliminating opponent
        this.DIRECTION.forEach(direction => {
            let adjPieceX = newX + direction[0];
            let adjPieceY = newY + direction[1];
            let adjPiece2X = adjPieceX + direction[0];
            let adjPiece2Y = adjPieceY + direction[1];

            if (this.isWithinBoard(adjPieceX,adjPieceY) &&
                this.get(adjPieceX,adjPieceY) == opponentColor && 
                this.isWithinBoard(adjPiece2X, adjPiece2Y) &&
                this.get(adjPiece2X,adjPiece2Y) in [ourColor, this.CELL_CORNER]) {
                
                this.set(adjPieceX,adjPieceY, this.CELL_EMPTY);
            }
        });

        // step 2: opponent eliminating ours

        if (this.isWithinBoard(newX -1, newY) && this.get(newX-1,newY) in [opponentColor, this.CELL_CORNER]
        && this.isWithinBoard(newX+1, newY)  && this.get(newX+1, newY) in [opponentColor, this.CELL_CORNER]) {
            this.set(newX,newY, this.CELL_EMPTY);
        }

        
        if (this.isWithinBoard(newX, newY-1) && this.get(newX,newY-1) in [opponentColor, this.CELL_CORNER]
        && this.isWithinBoard(newX, newY+1)  && this.get(newX, newY+1) in [opponentColor, this.CELL_CORNER]) {
            this.set(newX,newY, this.CELL_EMPTY);
        }
    }
}

export enum PlayerColor {
    Black,
    White
}
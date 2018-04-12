export class Board {
    private readonly BOARD_MAX_SIZE: number = 8;
    public static readonly CELL_EMPTY: string = ' ';
    public static readonly CELL_BLACK: string = 'B';
    public static readonly CELL_WHITE: string = 'W';
    public static readonly CELL_CORNER: string = 'X';
    public static readonly CELL_DEAD: string = 'D';

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
                row.push(Board.CELL_EMPTY);
            }
            this.board.push(row);
        }


        // current board size
        this.currentBoardSize = 8;
        this.updateCorners();
    }

    private getCorners(): Array<[number,number]> {
        return [
            [this.minX, this.minY],
            [this.minX, this.maxY],
            [this.maxX, this.minY],
            [this.maxX, this.maxY]
        ];
    }

    private updateCorners() {
        // set the corners
        this.getCorners().forEach(pos => {
            this.set(pos[0], pos[1], Board.CELL_CORNER);
        });
    }

    public set(x, y, value) {
        if (!this.isWithinBoard(x, y)) {
            throw `(${x},${y}) is not in board`;
        }
        this.board[x][y] = value;
    }

    public get(x, y): string {
        if (!this.isWithinBoard(x, y)) {
            return Board.CELL_DEAD;
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
        return (Number.isInteger(x) && Number.isInteger(y)) && (this.minX <= x && x <= this.maxX && this.minY <= y && y <= this.maxY);
    }

    public getWinner() : PlayerColor | null {
        if (this.checkWinning(PlayerColor.Black)) {
            return PlayerColor.Black;
        } else if (this.checkWinning(PlayerColor.White)) {
            return PlayerColor.White;
        } else {
            return null;
        }
    }

    private checkWinning(color: PlayerColor) {
        let colorStr = color == PlayerColor.Black ? Board.CELL_BLACK : Board.CELL_WHITE;
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
        if (myColor == Board.CELL_BLACK) {
            return Board.CELL_WHITE;
        } else {
            return Board.CELL_BLACK;
        }
    }


    public printBoard(): void {
        // for debug purposes
        for (var i = 0; i < this.BOARD_MAX_SIZE; ++i) {
            let row = '';
            for (var j = 0; j < this.BOARD_MAX_SIZE; ++j) {
                row += this.get(j, i) + ' '
            }
            console.log(row);
        }
    }

    public makeMove(fromPos: [number, number], toPos: [number, number]): void {
        var ourColor = this.get(fromPos[0], fromPos[1]);
        var opponentColor = this.getOpponentColor(ourColor);
        this.set(fromPos[0], fromPos[1], Board.CELL_EMPTY);
        this.set(toPos[0], toPos[1], ourColor);
        this.doElimination(toPos[0], toPos[1]);
    }

    public placeNewPiece(x, y, color) {
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
                this.get(adjPiece2X,adjPiece2Y) in [ourColor, Board.CELL_CORNER]) {
                
                this.set(adjPieceX,adjPieceY, Board.CELL_EMPTY);
            }
        });

        // step 2: opponent eliminating ours

        if (this.isWithinBoard(newX -1, newY) && this.get(newX-1,newY) in [opponentColor, Board.CELL_CORNER]
        && this.isWithinBoard(newX+1, newY)  && this.get(newX+1, newY) in [opponentColor, Board.CELL_CORNER]) {
            this.set(newX,newY, Board.CELL_EMPTY);
        }

        
        if (this.isWithinBoard(newX, newY-1) && this.get(newX,newY-1) in [opponentColor, Board.CELL_CORNER]
        && this.isWithinBoard(newX, newY+1)  && this.get(newX, newY+1) in [opponentColor, Board.CELL_CORNER]) {
            this.set(newX,newY, Board.CELL_EMPTY);
        }
    }

    public getMatrix(): Array<Array<string>> {
        return this.board;
    }

    public shrinkBoard() {
        if (this.currentBoardSize<=4) return;
        // clean the circle
        for (let i = this.minX; i<=this.maxX; ++i) {
            this.set(i, this.minY, Board.CELL_DEAD);
            this.set(i, this.maxY, Board.CELL_DEAD);
        }
        for (let i = this.minY+1; i<=this.maxY-1; ++i) {
            this.set(this.minX, i, Board.CELL_DEAD);
            this.set(this.maxX, i, Board.CELL_DEAD);
        }
        
        this.currentBoardSize -=2;
        this.updateCorners();
        // do the elimination
        this.getCorners().forEach(pos => {
            let x = pos[0];
            let y = pos[1];
            this.DIRECTION.forEach(direction => {
                let adjPieceX = x + direction[0];
                let adjPieceY = y + direction[1];
                let adjPiece2X = adjPieceX + direction[0];
                let adjPiece2Y = adjPieceY + direction[1];
    
                if (this.isWithinBoard(adjPieceX,adjPieceY) &&
                    this.get(adjPieceX,adjPieceY) in [Board.CELL_BLACK, Board.CELL_WHITE] && 
                    this.isWithinBoard(adjPiece2X, adjPiece2Y) &&
                    this.get(adjPiece2X,adjPiece2Y) in [Board.CELL_BLACK, Board.CELL_WHITE]) {
                    
                    if (this.get(adjPieceX, adjPieceY) != this.get(adjPiece2X, adjPiece2Y)){
                        this.set(adjPieceX,adjPieceY, Board.CELL_EMPTY);
                    }
                }
            });
    
        });


    }

    public isValidMove(fromPos:[number,number], toPos:[number,number]): boolean{
        function mean(a:number,b:number):number {
            return (a+b)/2;
        }
        return (this.isWithinBoard(fromPos[0],fromPos[1]) && this.isWithinBoard(toPos[0], toPos[1])
            && ([Board.CELL_BLACK, Board.CELL_WHITE].indexOf(this.get(fromPos[0], fromPos[1])) != -1)
            && (this.get(toPos[0],toPos[1]) == Board.CELL_EMPTY)
            && ( 
                (Math.abs(toPos[0]-fromPos[0])+ Math.abs(toPos[1]-fromPos[1]) == 1) // adjacent
                || (Math.abs(toPos[0]-fromPos[0])+ Math.abs(toPos[1]-fromPos[1]) == 2 // two steps away
                    && Math.abs(toPos[0]-fromPos[0])*Math.abs(toPos[1]-fromPos[1])== 0 // not diagonal
                    && this.get(fromPos[0], fromPos[1]) == this.get(mean(fromPos[0],toPos[0]),mean(fromPos[1],toPos[1]))) // adj == adj2
                )
        );
    }

    public canPlace(x: number, y:number, color:string): boolean {
        if (!(this.isWithinBoard(x,y) && this.get(x,y) == Board.CELL_EMPTY)) {
            return false;
        }
        if (color == Board.CELL_WHITE && y<=5) return true;
        if (color == Board.CELL_BLACK && y>=2) return true;
        return false;
    }
}

export enum PlayerColor {
    Black,
    White
}
import { PlayerColor, Board, PlayerAction, Player, PlayerActionResult, PlayerActionType, PlayerPlaceAction, PlayerMoveAction} from "./";
import { setImmediate } from "timers";

export class GameSession {

    // @todo: double check spec
    private readonly upperHand : PlayerColor = PlayerColor.Black;
    private readonly NUMBER_OF_PIECES : number = 12;


    private id : string;
    private turn : PlayerColor;

    private round = 0; // counts through both placing and moving phases
    private board: Board = new Board();
    private startTime: Date;
    private roundStartTime: Date;
    private phase: GamePhase;
    private whiteToPlace: number;
    private blackToPlace: number;
    private moveCount: number; // only counts moving phase
    private ended :boolean = false;
    private actions: Array<[number, PlayerColor, PlayerAction]>;

    constructor (id:string){
        this.id = id;
        console.log(`New GameSession ${id}`);
    }

    public getId(): string {
        return this.id;
    }

    public start() {
        this.startTime = new Date(Date.now());
        this.round = 0;
        this.moveCount = 0;
        this.actions = [];
        this.nextRound();
    }

    public tryTakeAction(act:PlayerAction, color:PlayerColor):PlayerActionResult {
        if (this.ended) return PlayerActionResult.failed("Game ended.");
        console.log('color',color)
        if (this.turn != color) return PlayerActionResult.failed("Not your turn.");

        let colorStr = (color == PlayerColor.Black)?Board.CELL_BLACK:Board.CELL_WHITE;
        if (this.phase == GamePhase.Placing && act.type == PlayerActionType.Place) {
            // handling placing
            let a = (act as PlayerPlaceAction);
            if (! this.board.canPlace(a.newX,a.newY,colorStr) ) {
                return PlayerActionResult.failed("Cannot place pieces here.")
            }
            this.board.placeNewPiece(a.newX,a.newY,colorStr);
            if (color == PlayerColor.Black) {
                --this.blackToPlace;
            } else {
                --this.whiteToPlace;
            }
            this.actions.push([this.round, color, act]);
            setImmediate(()=> this.nextRound());
            setImmediate(()=> this.sendUpdate({
                lastMove: this.actions[this.actions.length-1],
                timeSinceStart: this.getTime(),
                phase: this.phase,
                timeLeftForThisTurn: -1
            }));
            return PlayerActionResult.success();
        } else if (this.phase == GamePhase.Moving && act.type == PlayerActionType.MakeMove) {
            // handling moving
            let a = (act as PlayerMoveAction);
            let fromP :[number, number]=[a.fromX, a.fromY];
            let toP :[number, number]= [a.toX, a.toY];
            if (!( this.board.get(a.fromX,a.fromY) == colorStr && this.board.isValidMove(fromP,toP)) ) {
                return PlayerActionResult.failed("Invalid move. Try again.");
            }
            this.board.makeMove(fromP,toP);
            this.actions.push([this.round,color,act]);
            this.moveCount ++;
            setImmediate(()=> this.nextRound());
            return PlayerActionResult.success();
        } else {
            return PlayerActionResult.failed("Invalid action type.");
        }
    }

    public nextRound() {
        if (this.ended) return;
        //DEBUG
        console.log("Round "+this.round);
        this.board.printBoard();
        console.log("")
        console.log("")

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
                setImmediate(()=> this.pushSync());
            }
            
            this.round++;
            this.roundStartTime = new Date(Date.now());
        } else if (this.phase == GamePhase.Placing) {
            if (this.whiteToPlace == 0 && this.blackToPlace == 0){
                // placing phase ended
                this.phase = GamePhase.Moving;
                this.turn = this.upperHand;
                this.roundStartTime = new Date(Date.now());
                setImmediate(()=>this.pushSync());
            } else {
                this.turn = (this.turn == PlayerColor.Black) ? PlayerColor.White : PlayerColor.Black;
            }
            
            this.round++;
        }
    }

    private getTime() : number {
        // seconds since the start of the game
        var now = new Date(Date.now());
        return (now.getTime() - this.startTime.getTime())/1000;
    }

    public getSyncObject() : GameSessionSync {
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
    }

    public onUpdate: Function;
    public onPushSync: Function;

    private sendUpdate(u: GameSessionUpdate) {
        if (this.onUpdate) {
            this.onUpdate(u); // what to send?
        }
    }

    private pushSync() {
        if (this.onPushSync) {
            let s = this.getSyncObject();
            this.onPushSync(s);
        }
    }
}

export interface GameSessionUpdate {
    timeLeftForThisTurn: number; //seconds; -1 for unlimited
    timeSinceStart: number; //seconds,
    lastMove: [number, PlayerColor, PlayerAction];
    phase: GamePhase;
}

export interface GameSessionSync {
    board: Array<Array<string>>;
    round: number;
    turn: PlayerColor;
    winner: PlayerColor|null;
    phase: GamePhase;
    timeLeftForThisTurn: number; //seconds
    timeSinceStart: number; //seconds
    listOfMoves: Array<[number, PlayerColor, PlayerAction]>;
}


export enum GamePhase {
    Placing,
    Moving
}
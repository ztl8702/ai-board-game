import { GameRoom } from "./GameRoom";

export class Player {
    // Representation of each player in the game
    private id : string;
    private ipAddress: string;
    private userAgent: string;
    private lastSeen: Date;
    private firstSeen: Date;
    private _nickName: string;
    public get nickName():string {
        return this._nickName;
    }
    public set nickName(value:string){
        this._nickName = value;
    }

    private gameRoom: GameRoom;
    private state : PlayerState;

    private socketIO: any;
    
    constructor (id:string) {
        this.id = id;
    }


    public notifyStart() {
        if (this.socketIO) {
            this.socketIO.emit('gameStarted');
        }
    }

    public setSocket(socket: any) {
        this.socketIO = socket;
    }


    // actions
    public tryJoinRoom(roomId: string):boolean {
        return false;
    }

    public leaveRoom() {
        if (this.state == PlayerState.JoinedAsPlayer) {
            this.gameRoom.removePlayer(this);
        } else if (this.state == PlayerState.JoinedAsObserver) {
           // this.gameRoom.removeObserver(this);
        }
    }

    public observeRoom(roomId: string){

    }

    public tryTakeAction() {
        if (this.state == PlayerState.JoinedAsPlayer) {
            let result = this.gameRoom.tryTakeAction();
        }
    }

    public newSession() {

    }

    public startGame() {

    }

}

enum PlayerState {
    NoRoom,
    JoinedAsPlayer,
    JoinedAsObserver
}

class PlayerAction {
    public type: PlayerActionType;
}

class PlayerPlaceAction extends PlayerAction {
    public newX: number;
    public newY: number;
    public type: PlayerActionType = PlayerActionType.Place;
}

class PlayerMoveAction extends PlayerAction {
    public fromX: number;
    public fromY: number;
    public toX: number;
    public toY: number;
    public type: PlayerActionType = PlayerActionType.MakeMove;
}

class PlayActionResult {
    public isSuccess: boolean;
    public message: string;

    constructor(isSucess:boolean) {
        this.isSuccess = true;
    }
    
}

enum PlayerActionType {
    Place,
    MakeMove
}
import { GameRoom } from "./GameRoom";
import { ActorFactory } from "../actor/index";
import * as faker from "faker";

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
        this.state = PlayerState.NoRoom;
        this.nickName = faker.name.findName(); // create a random name
        console.log(`New Player ${this.nickName} (${this.id}). `);
    }

    public getId(): string {
        return this.id;
    }

    public notifyStart() {
        if (this.socketIO) {
            this.socketIO.emit('gameStarted');
        }
    }

    public setSocket(socket: any) {
        this.socketIO = socket;
    }

    public removeSocket() {
        this.socketIO = null;
    }

    // actions
    public tryJoinRoom(roomId: string):boolean {
        if (this.state == PlayerState.NoRoom) {
            var room = ActorFactory.getActor('GameRoom', roomId) as GameRoom;
            var result = room.addPlayer(this);
            if (result) {
                this.state = PlayerState.JoinedAsPlayer;
                this.gameRoom = room;
            }
            return result;
        } else {
            return false;
        }
    }

    public leaveRoom() {
        if (this.state == PlayerState.JoinedAsPlayer) {
            this.gameRoom.removePlayer(this);
            this.gameRoom = null;
            this.state = PlayerState.NoRoom;
        } else if (this.state == PlayerState.JoinedAsObserver) {
            this.gameRoom.removeObserver(this);
            this.gameRoom = null;
            this.state = PlayerState.NoRoom;
        }
    }

    public observeRoom(roomId: string){
        if (this.state == PlayerState.NoRoom){
            var room = ActorFactory.getActor('GameRoom', roomId) as GameRoom;
            room.addObserver(this);
            this.gameRoom = room;
            this.state = PlayerState.JoinedAsObserver;
        }
    }

    public tryTakeAction(a: PlayerAction):PlayerActionResult {
        if (this.state == PlayerState.JoinedAsPlayer) {
            let result = this.gameRoom.tryTakeAction(a, this);
            return result;
        }
        return PlayerActionResult.failed("You are not in a room.")
    }

    public newSession() {

    }

    public tryStartGame() {
        if (this.state == PlayerState.JoinedAsPlayer) {
            this.gameRoom.startGame();
        }
    }

    public send(...args: any[]) {
        if (this.socketIO != null) {
            this.socketIO.emit(...args);
        }
    }

}

enum PlayerState {
    NoRoom,
    JoinedAsPlayer,
    JoinedAsObserver
}

export enum PlayerActionType {
    Place,
    MakeMove
}

export class PlayerAction {
    public type: PlayerActionType;
}

export interface PlayerPlaceAction extends PlayerAction {
    newX: number;
    newY: number;
    type: PlayerActionType.Place;
}

export interface PlayerMoveAction extends PlayerAction {
    fromX: number;
    fromY: number;
    toX: number;
    toY: number;
    type: PlayerActionType.MakeMove;
}

export class PlayerActionResult {
    public isSuccess: boolean;
    public message: string;

    constructor(isSuccess:boolean) {
        this.isSuccess = isSuccess;
    }

    public static success(): PlayerActionResult {
        return new PlayerActionResult(true);
    }

    public static failed(reason:string): PlayerActionResult {
        var result = new PlayerActionResult(false);
        result.message = reason;
        return result;
    }
    
}

export interface PlayerSync {
    state: PlayerState,
    roomId: string|null,
    id: string,
    nickName: string
}
import { PlayerColor, Board } from "./Board";
import { Player } from "./Player";
import { GameSession, GameSessionSync, PlayerAction, PlayerActionResult, GameSessionUpdate } from "./";
import { ActorFactory } from "../actor/index";

export class GameRoom {
    // representation of each game play
    private id: string;
    private state: GameRoomState;


    private playerCount = 0;
    private whitePlayer: Player;
    private blackPlayer: Player;
    private observers: Array<Player>;
    private currentSession: GameSession;

    constructor(id: string) {
        console.log("GameRoom", id, "created.");
        this.id = id;
        this.state = GameRoomState.WaitingForPlayers;
        this.observers = [];
        this.currentSession = this.currentSession = ActorFactory.getActor("GameSession", null);
        this.currentSession.onPushSync = ()=>{this.broadcastSessionSync();};
        this.currentSession.onUpdate = (u)=> this.broadcastSessionUpdate(u);
    }

    public isFull(): boolean {
        return this.playerCount >= 2;
    }


    public addPlayer(newPlayer: Player):boolean {
        var result :boolean = false;

        switch (this.state) {
            case GameRoomState.WaitingForPlayers:
                // black player first
                if (this.playerCount == 0) {
                    this.blackPlayer = newPlayer;
                    ++this.playerCount;
                    result = true;
                    console.log("Player "+newPlayer.nickName+" joined GameRoom "+ this.id+" as black player.");
                } else if (this.playerCount == 1) {
                    this.whitePlayer = newPlayer;
                    ++this.playerCount;
                    result = true;
                    console.log("Player "+newPlayer.nickName+" joined GameRoom "+ this.id+" as white player.");                    
                }
                if (this.playerCount == 2) {
                    this.changeState(GameRoomState.Ready);
                }
                this.broadcastRoomSync();
                break;
        }
        return result;

    }

    public removePlayer(player: Player) {

        function doRemovePlayer(player: Player) {
            if (player == this.blackPlayer) {
                this.blackPlayer = null;
                this.playerCount--;
            } else if (player == this.whitePlayer) {
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
            case GameRoomState.WaitingForPlayers:
            case GameRoomState.DisplayResult:
                doRemovePlayer(player);
                break;

            case GameRoomState.Ready:
                doRemovePlayer(player);
                this.changeState(GameRoomState.WaitingForPlayers);
                break;
                
        }
        this.broadcastRoomSync();
    }

    public addObserver(obs: Player) {
        if ( this.observers.indexOf(obs) == -1) {
            this.observers.push(obs);
        }
        this.broadcastRoomSync();
    }

    public removeObserver(obs: Player) {
        var index = this.observers.indexOf(obs);
        if ( index != -1) {
            this.observers.splice(index, 1);
        }
        this.broadcastRoomSync();
    }

    public startGame() {
        if (this.state == GameRoomState.Ready) {
            this.currentSession.start();
            this.changeState(GameRoomState.Playing);
            this.broadcastRoomSync();
            this.broadcastSessionSync();
        }
    }

    private broadcastRoomSync() {
        // Send room sync to all players and observers
        var roomSync : GameRoomSync = this.getSyncObject();
        function sendRoomSyncToPlayer(p:Player, rs: GameRoomSync) {
            p.send('roomSync', rs);
        }
        if (this.blackPlayer) sendRoomSyncToPlayer(this.blackPlayer,roomSync);
        if (this.whitePlayer) sendRoomSyncToPlayer(this.whitePlayer,roomSync);
        this.observers.forEach(obs => {
            sendRoomSyncToPlayer(obs, roomSync);
        });
    }

    private broadcastSessionSync() {
        var s = this.currentSession.getSyncObject();
        function sendRoomSyncToPlayer(p:Player, rs: GameSessionSync) {
            p.send('sessionSync', rs);
        }
        if (this.blackPlayer) sendRoomSyncToPlayer(this.blackPlayer,s);
        if (this.whitePlayer) sendRoomSyncToPlayer(this.whitePlayer,s);
        this.observers.forEach(obs => {
            sendRoomSyncToPlayer(obs, s);
        });
    }

    private broadcastSessionUpdate(u:GameSessionUpdate) {
        function sendRoomSyncToPlayer(p:Player, rs: GameSessionUpdate) {
            p.send('sessionUpdate', rs);
        }
        if (this.blackPlayer) sendRoomSyncToPlayer(this.blackPlayer,u);
        if (this.whitePlayer) sendRoomSyncToPlayer(this.whitePlayer,u);
        this.observers.forEach(obs => {
            sendRoomSyncToPlayer(obs, u);
        });
    }


    public getLatestResult() {

    }

    public newSession() {
        if (this.state == GameRoomState.DisplayResult || this.state == GameRoomState.Playing) {
            this.currentSession.onPushSync = null;
            this.currentSession.onUpdate = null;
            ActorFactory.archiveActor("GameSession", this.currentSession.getId());
            
            this.currentSession = ActorFactory.getActor("GameSession", null);
            this.currentSession.onPushSync = ()=>{this.broadcastSessionSync();};
            this.currentSession.onUpdate = (u)=> this.broadcastSessionUpdate(u);
            if (this.isFull()) {
                this.changeState(GameRoomState.Ready);
            } else {
                this.changeState(GameRoomState.WaitingForPlayers);
            }
        }
    }

    public getSessionSyncObject() : GameSessionSync {
        return this.currentSession.getSyncObject();
    }

    public getSyncObject(): GameRoomSync {
        var result : GameRoomSync = {
            blackPlayerId: this.blackPlayer ? this.blackPlayer.getId() : null,
            blackPlayerName: this.blackPlayer ? this.blackPlayer.nickName : null,
            whitePlayerId: this.whitePlayer ? this.whitePlayer.getId() :null,
            whitePlayerName: this.whitePlayer ? this.whitePlayer.nickName : null,
            state: this.state,
            observersCount: this.observers.length
        }
        return result;
    }

    private changeState(newState: GameRoomState) {
        if (newState != this.state) {
            this.state = newState;
            // notify players

        }
    }

    private whichPlayer(p: Player): PlayerColor|null {
        if (p == this.whitePlayer) return PlayerColor.White;
        if (p == this.blackPlayer) return PlayerColor.Black;
        return null;
    }

    public tryTakeAction(act: PlayerAction, caller: Player): PlayerActionResult {
        if (this.state != GameRoomState.Playing) {
            var result = new PlayerActionResult(false);
            result.message = "Game is not started."
            return result;
        }
        let side = this.whichPlayer(caller);
        if (side == null) {
            var result = new PlayerActionResult(false);
            result.message = "You are not playing in this room."
            return result;
        }

        var result = this.currentSession.tryTakeAction(act,side);
        return result;
    }

}

export enum GameRoomState {
    WaitingForPlayers,
    Ready,
    Playing,
    DisplayResult
}

export interface GameRoomSync {
    blackPlayerName: string;
    blackPlayerId: string;
    whitePlayerName: string;
    whitePlayerId: string;
    observersCount:number;
  // board: GameSessionSync;
    state: GameRoomState;
}






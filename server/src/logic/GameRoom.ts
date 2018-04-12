import { PlayerColor, Board } from "./Board";
import { Player } from "./Player";
import { GameSession } from "./";

export class GameRoom {
    // representation of each game play
    private id: string;
    private state: GameState;


    private playerCount = 0;
    private whitePlayer: Player;
    private blackPlayer: Player;
    private currentSession: GameSession;

    constructor(id: string) {
        this.id = id;
    }

    public isFull(): boolean {
        return this.playerCount >= 2;
    }


    public addPlayer(newPlayer: Player) {
        // black player first
        if (this.playerCount == 0) {
            this.blackPlayer = newPlayer;
            ++this.playerCount;
        } else if (this.playerCount == 1) {
            this.whitePlayer = newPlayer;
            ++this.playerCount;
        }
        switch (this.state) {
            case GameState.WaitingForPlayers:
                if (this.playerCount == 2) {
                    this.changeState(GameState.Ready);
                }
                break;
        }

    }

    public removePlayer(player: Player) {
        switch (this.state) {
            case GameState.Playing:
                // the game is ongoing
                if (player == this.blackPlayer) {
                    this.blackPlayer = null;
                    this.playerCount--;
                } else if (player == this.whitePlayer) {
                    this.whitePlayer = null;
                    this.playerCount--;
                }
                this.changeState(GameState.DisplayResult);

                break;
            case GameState.WaitingForPlayers, GameState.DisplayResult:
                if (player == this.blackPlayer) {
                    this.blackPlayer = null;
                    this.playerCount--;
                } else if (player == this.whitePlayer) {
                    this.whitePlayer = null;
                    this.playerCount--;
                }
                break;
        }
    }

    public startGame() {

    }

    public getLatestResult() {

    }

    public newSession() {
        
    }

    public getCurrentBoardState() : GameBoardState {

    }

    private changeState(newState: GameState) {
        if (newState != this.state) {
            this.state = newState;
            // notify players

        }
    }

}

enum GameState {
    WaitingForPlayers,
    Ready,
    Playing,
    DisplayResult
}

interface GameBoardState {
    board: Array<Array<string>>;
    round: number;
    turn: PlayerColor;
    hasWon: boolean;
    winner: PlayerColor;
    timeLeftForThisTurn: TimeRanges;
    timeSinceStart: TimeRanges;
}
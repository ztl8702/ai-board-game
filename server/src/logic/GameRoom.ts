import { PlayerColor } from "./Board";

class GameRoom {
    // representation for each game play
    private state : GameState;

    private turn : PlayerColor;

    private round = 0;

    
}

enum GameState {
    WaitingForPlayers,
    Playing,
    DisplayResult
}
import { GameSessionSync, GameRoom, GameRoomSync, Board } from "../../src/logic";

export class ClientViewModel {
    public page: string = 'welcome';
    public roomId: string;
    public playerId: string;
    public playerName: string;
    public roomInfo : GameRoomSync = null;
    public sessionInfo : GameSessionSync= null;
    public board: Board;
}

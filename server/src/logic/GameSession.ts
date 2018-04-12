import { PlayerColor, Board } from "./";

export class GameSession {

    private id : string;
    private turn : PlayerColor;

    private round = 0;
    private board: Board = new Board();

    constructor (id:string){
        this.id = id;
    }
}
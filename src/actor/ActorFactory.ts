import {GameRoom, Player, GameSession} from "../logic";
var cryptol = require("crypto");



export class ActorFactory {
    private static dict = {
        'GameRoom': {},
        'Player': {},
        'GameSession': {}
    }

    public static getActor(type:string, id: string) :any {
        if (id == null || id == ''){
            // generate random id
            id = cryptol.randomBytes(16).toString("hex");
        }
        if (this.dict[type][id] == null) {
            switch (type) {
                case 'GameRoom':
                    this.dict[type][id] = new GameRoom(id);
                    break;
                case 'GameSession':
                    this.dict[type][id] = new GameSession(id);
                    break;
                case 'Player':
                    this.dict[type][id] = new Player(id);
                    break;
            }
        }
        return this.dict[type][id];
    }

    public static archiveActor(type:string, id:string) {

    }
}
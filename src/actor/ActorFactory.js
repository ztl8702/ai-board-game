"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
var logic_1 = require("../logic");
var cryptol = require("crypto");
var ActorFactory = /** @class */ (function () {
    function ActorFactory() {
    }
    ActorFactory.getActor = function (type, id) {
        if (id == null || id == '') {
            // generate random id
            id = cryptol.randomBytes(16).toString("hex");
        }
        if (this.dict[type][id] == null) {
            switch (type) {
                case 'GameRoom':
                    this.dict[type][id] = new logic_1.GameRoom(id);
                    break;
                case 'GameSession':
                    this.dict[type][id] = new logic_1.GameSession(id);
                    break;
                case 'Player':
                    this.dict[type][id] = new logic_1.Player(id);
                    break;
            }
        }
        return this.dict[type][id];
    };
    ActorFactory.archiveActor = function (type, id) {
    };
    ActorFactory.dict = {
        'GameRoom': {},
        'Player': {},
        'GameSession': {}
    };
    return ActorFactory;
}());
exports.ActorFactory = ActorFactory;

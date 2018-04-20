import * as Sequelize from 'sequelize';
import { GameSession, PlayerAction } from '../logic';
import { isProduction, getEnv } from '../util';

// test only. change for production
var connString : string;

if (isProduction()) {
    connString = getEnv("WYB_DB");
} else {
    connString = 'postgres://postgres:password@localhost:5432/wyb';
}
const sequelize = new Sequelize(connString);

export class DBConnection {

    async test(): Promise<boolean> {
        var p = sequelize.authenticate();
        try {
            await p;
            return true;
        } catch (e) {
            console.error("Error conn:", e);
            return false;
        }
    }

    async saveGameSession(s: GameSession, white: string, black: string): Promise<void> {
        await Session.create({
            id: s.getId(),
            whitePlayerId: white,
            blackPlayerId: black,
            winner: s.getSyncObject().winner
        });

        for (let a of s.actions) {
            await GameMove.create({
                session: s.getId(),
                side: a[1],
                sequence: a[0],
                moveType: a[2].type,
                moveArgs: a[2]
            })
        }

    }

    migrate() {
        Session.sync().then(_ => {
            console.log('Migration succeed for Session');
        }).catch(e => {
            console.error('Migration Error', e
            )
        })
        GameMove.sync().then(_ => {
            console.log('Migration succeed for GameMove');
        }).catch(e => {
            console.error('Migration Error', e
            )
        })
    }
}


export const Session = sequelize.define('gamesession', {
    id: {
        type: Sequelize.STRING,
        primaryKey: true
    },
    time: {
        type: Sequelize.DATE
    },
    blackPlayerId: {
        type: Sequelize.STRING
    },
    whitePlayerId: {
        type: Sequelize.STRING
    },
    winner: {
        type: Sequelize.STRING
    }
});
export const GameMove = sequelize.define('gamemove', {
    session: {
        type: Sequelize.STRING,
        unique: 'compositeIndex'
    },
    sequence: {
        type: Sequelize.INTEGER,
        unique: 'compositeIndex'
    },
    side: {
        type: Sequelize.SMALLINT,
    },
    moveType: {
        type: Sequelize.SMALLINT
    },
    moveArgs: {
        type: Sequelize.JSON
    }
});
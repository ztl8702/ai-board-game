import { PlayerActionType } from "../../src/logic";

declare var io: any;
export class Socket {
    static socket = io();
    static initialize() {

        Socket.socket.on('roomSync', function (d) {
            console.log('roomSync', d);
            if (Socket.onRoomSync) {
                Socket.onRoomSync(d);
            }
        });

        Socket.socket.on('sessionSync', function (d) {
            console.log('sessionSync', d);
            if (Socket.onSessionSync) {
                Socket.onSessionSync(d);
            }
        });

        Socket.socket.on('sessionUpdate', function (d) {
            console.log('sessionUpdate', d);
            if (Socket.onSessionUpdate) {
                Socket.onSessionUpdate(d);
            }
        });

        Socket.socket.on('playerSync', function (d) {
            console.log('playerSync', d,'the callback is', Socket.onPlayerSync);
            if (Socket.onPlayerSync) {
                Socket.onPlayerSync(d);
            }
        });
        
    }

    public static startGame() {
        this.socket.emit('startGame');
    }

    public static joinRoom(roomId) {
        this.socket.emit('joinRoom', roomId);
    }
    
    public static observeRoom(roomId) {
        this.socket.emit('observeRoom', roomId);
    }

    public static placePiece(x, y) {
        this.socket.emit('makeMove',{ 
            type: PlayerActionType.Place, 
            newX: x, 
            newY: y 
        },
        function (d) { console.log(d) });
    }

    public static movePiece(x1, y1, x2, y2) {
        this.socket.emit('makeMove', { 
            type: PlayerActionType.MakeMove, 
            fromX: x1, 
            fromY: y1, 
            toX: x2, 
            toY: y2 
        },
        function (d) { console.log(d) });
    
    }
    public static newSession() {
        this.socket.emit('newSession' );
    }

    public static requestRoomSync(roomId) {
        this.socket.emit('roomSyncRequest',roomId);
    }

    public static setNickname(newNickname) {
        this.socket.emit('setNickname', newNickname);
    }

    public static requestSessionSync(roomId) {
        this.socket.emit('sessionSyncRequest',roomId);
    }


    public static requestPlayerSync() {
        this.socket.emit('playerSyncRequest');
    }

    public static leaveRoom() {
        this.socket.emit('leaveRoom');
    }

    public static onRoomSync : Function;
    public static onSessionSync: Function;
    public static onPlayerSync: Function;
    public static onSessionUpdate: Function;
}

Socket.initialize();
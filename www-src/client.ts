import { Board, PlayerSync, PlayerState, GameRoomSync, GameRoomState, GameSessionSync, GameSessionUpdate, PlayerActionType, PlayerPlaceAction, PlayerMoveAction, PlayerColor } from "../src/logic"

import { App } from "./App";
import { Socket } from "./utils";
import { setInterval } from "timers";

var myApp: any = new App({ el: '#app' });

myApp.vm.board = new Board();
console.log('App loaded');

Socket.onPlayerSync = (playerInfo: PlayerSync) => {
    console.log('playerSync callback');
    myApp.vm.playerId = playerInfo.id;
    myApp.vm.playerName = playerInfo.nickName;
    switch (playerInfo.state) {
        case PlayerState.NoRoom:
            myApp.vm.page = 'welcome';
            break;
        case PlayerState.JoinedAsObserver:
        case PlayerState.JoinedAsPlayer:
            if (myApp.vm.page == 'welcome') myApp.vm.page = 'room';
            break;
    }
    myApp.vm.roomId = playerInfo.roomId;
    if (myApp.vm.roomId) {
        Socket.requestRoomSync(myApp.vm.roomId);
    }
    myApp.$forceUpdate();
};

Socket.onRoomSync = (roomInfo: GameRoomSync) => {
    myApp.vm.roomInfo = roomInfo;
    if (roomInfo.state == GameRoomState.Playing || roomInfo.state == GameRoomState.DisplayResult) {
        myApp.vm.page = 'board';
        Socket.requestSessionSync(myApp.vm.roomId);
    } else {
        myApp.vm.page = 'room';
    }
    myApp.$forceUpdate();
}

function recursiveUpdate(vueComponent) {
    vueComponent.$forceUpdate();
    vueComponent.$children.forEach(child => {
        recursiveUpdate(child)
    });

}
Socket.onSessionSync = (sessionInfo: GameSessionSync) => {
    myApp.vm.sessionInfo = sessionInfo;
    myApp.vm.board = Board.fromMatrix(sessionInfo.board);
    recursiveUpdate(myApp);
    myApp.vm.sessionInfo.round++;
    recursiveUpdate(myApp);
    myApp.vm.sessionInfo.round--;
    recursiveUpdate(myApp);

}


Socket.onSessionUpdate = (sessionUpdate: GameSessionUpdate) => {
    var lastMoveId = 0;
    if (myApp.vm.sessionInfo.listOfMoves.length > 0) {
        lastMoveId = myApp.vm.sessionInfo.listOfMoves[myApp.vm.sessionInfo.listOfMoves.length - 1][0];
    }
    if (lastMoveId >= sessionUpdate.lastMove[0]) {
        // do nothing
    } else if (lastMoveId == sessionUpdate.lastMove[0] - 1 && sessionUpdate.phase == myApp.vm.sessionInfo.phase) {
        myApp.vm.sessionInfo.listOfMoves.push(sessionUpdate.lastMove);
        if (sessionUpdate.lastMove[2].type == PlayerActionType.Place) {
            (myApp.vm.board as Board).placeNewPiece(
                (sessionUpdate.lastMove[2] as PlayerPlaceAction).newX,
                (sessionUpdate.lastMove[2] as PlayerPlaceAction).newY,
                sessionUpdate.lastMove[1] == PlayerColor.Black ? Board.CELL_BLACK : Board.CELL_WHITE
            );

        } else if (sessionUpdate.lastMove[2].type == PlayerActionType.MakeMove) {
            var act = sessionUpdate.lastMove[2] as PlayerMoveAction;
            (myApp.vm.board as Board).makeMove([act.fromX, act.fromY], [act.toX, act.toY]);
        }
        myApp.vm.sessionInfo.turn = myApp.vm.sessionInfo.turn == PlayerColor.Black ? PlayerColor.White : PlayerColor.Black;
        ++myApp.vm.sessionInfo.round;

    } else {
        // out of sync
        Socket.requestSessionSync(myApp.vm.roomId);
    }

    myApp.$forceUpdate();
}
Socket.requestPlayerSync();



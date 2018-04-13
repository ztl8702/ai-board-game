import { Board } from "../src/logic"
import * as faker from "faker";
import "./components/App";
declare var io:any;

function getRandomRoomId() {
    var str = faker.hacker.adjective() + '_' + faker.hacker.noun();
    str.replace(/ /g, '_');
    str.replace(/-/g, '_');
    return str;
}


var socket = io();
socket.on('roomSync', function (d) {
    console.log('roomSync', d);
})
socket.on('sessionSync', function (d) {
    console.log('sessionSync', d);
})
socket.on('sessionUpdate', function (d) {
    console.log('sessionUpdate', d);
})
socket.emit('roomSyncRequest');
function joinRoom(roomId) {
    socket.emit('joinRoom', roomId);
}
function startGame() {
    socket.emit('startGame');
}
function placePiece(x, y) {
    socket.emit('makeMove',
        { type: 0, newX: x, newY: y },
        function (d) { console.log(d) });

}

function movePiece(x1, y1, x2, y2) {
    socket.emit('makeMove',
        { type: 1, fromX: x1, fromY: y1, toX: x2, toY: y2 },
        function (d) { console.log(d) });

}
console.log(getRandomRoomId());

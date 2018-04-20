import Vue from 'vue';
import Component from "vue-class-component";
import { Prop } from "vue-property-decorator";
import { Socket } from '../utils';
import { PlayBoard, PlayBoardMode, PlacingProgressBar, WhosTurn, MovingProgress, MyDimmer } from "../components";
import { ClientViewModel } from '../models/ClientViewModel';
import { GamePhase, PlayerColor, PlayerActionType, Player, Board, PlayerMoveAction, PlayerPlaceAction, PlayerAction, GameSession } from '../../src/logic';
declare var $: any;


@Component({
    name: 'board-page',
    template: `
    <div class="ui grid stackable doubling container">
        <my-dimmer v-if="hasWinner" >
            <i class="heart icon"></i>
            Winner is {{winnerName}}! <button @click="onReturnClicked">Return to room</button>
        </my-dimmer>
        <my-dimmer v-if="!hasWinner && hasEnded" >
            Game ended because your opponent quitted. <button class="ui huge button" @click="onReturnClicked">Return to room</button>
        </my-dimmer>
        <div class="two column row">
            <div class="nine wide column">
                <play-board 
                    v-bind:mode="theMode" 
                    v-bind:board="viewModel.board" 
                    v-bind:playerColor="playerColor" 
                    v-model="boardOutput"
                    v-bind:rotate="shouldRotateBoard"
                    v-bind:lastMove="lastMove" 
                    v-bind:allowedRowStart="allowedRows[0]"
                    v-bind:allowedRowEnd="allowedRows[1]"
                />
            </div>
            <div class="seven wide column">
                <div class="ui segment" v-if="hasWinner==false">
                    <whos-turn v-bind:yours="myTurn" v-bind:oppo="!myTurn && !hasWinner" />
                    <placing-progress-bar 
                        v-bind:progress="viewModel.sessionInfo.round-1" 
                        v-if="isPlacing" />
                    <moving-progress
                        v-if="isMoving" 
                        v-bind:mine="myPiecesCount"
                        v-bind:oppo="oppoPiecesCount"
                    />
                </div>
                <div class="ui segment">
                    <h2>Room {{viewModel.roomId}} <button class="ui button" @click="onQuit">Quit</button></h2>
                    <h3> {{sideText}}</h3>
                    <h3> {{getPhaseString()}} Turn #{{turnNumber}}</h3>
                    <a class="ui red label" v-if="showWarning">Board about to shrink</a>
                </div>
                <div class="ui segment" v-if="myTurn">
                    <p v-if="showButton">{{previewMove}}</p>
                    <button @click="onSubmit" class="ui blue button" v-if="showButton">Submit (Enter)</button>
                    <button @click="onPass" class="ui yellow button" v-if="isMoving" >Pass</button>
                </div>
            </div>
        </div>
        <div class="one column row">
            <div class="column" style="max-height:200px; overflow-y:scroll; overflow-x:hidden;">
                <table class="ui single line table">
                    <thead>
                        <tr>
                        <th>#</th>
                        <th>Move</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr v-for="(move,index) in listOfMoves.slice().reverse()">
                        <td>{{move[0]}}</td>
                        <td>{{move[1]}}</td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>

    </div>`,
    components: { PlayBoard, PlacingProgressBar, WhosTurn, MovingProgress, MyDimmer }
})
export class BoardPage extends Vue {
    @Prop()
    viewModel: ClientViewModel;


    boardOutput = null;
    constructor() {
        super();
    }

    get theBoard() {
        return this.viewModel.board;
    }
    updated() {
        console.log('BoardPage updated. updating children.')
        this.$children.forEach(child => {
            child.$forceUpdate();
        });
    }
    mounted() {

        Socket.requestSessionSync(this.viewModel.roomId);
        window.addEventListener('keydown', this.onKeyPress);
    }

    onKeyPress(e) {
        console.log(e.keyCode);
        if (e.keyCode == 13 && this.boardOutput) {
            if (confirm("Are you sure you want to submit this move?")) this.onSubmit();
        }
    }

    beforeDestroy() {
        window.removeEventListener('keydown', this.onKeyPress);
    }
    getPhaseString() {
        try {
            if (this.viewModel.sessionInfo.phase == GamePhase.Moving) {
                return "Moving phase"
            }
            else {
                return "Placing phase"
            }
        } catch {
            return "";
        }

    }
    get turnNumber() {
        if (this.isPlacing) return (this.viewModel.sessionInfo.round);
        if (this.isMoving) return (this.viewModel.sessionInfo.round - GameSession.NUMBER_OF_PIECES * 2);
    }

    get showWarning() {
        if (this.isMoving) {
            if (this.turnNumber == GameSession.FIRST_SHRINK
                || this.turnNumber == GameSession.SECOND_SHRINK) {
                return true;
            }
        }
        return false;
    }

    get shouldRotateBoard(): boolean {
        return this.side() == PlayerColor.White;
    }

    get isPlacing(): boolean {
        try {
            if (this.viewModel.sessionInfo.phase == GamePhase.Placing) {
                return true;
            }
        } catch {

        }
        return false;
    }

    get isMoving(): boolean {
        try {
            if (this.viewModel.sessionInfo.phase == GamePhase.Moving) {
                return true;
            }
        } catch {

        }
        return false;
    }

    side(): PlayerColor {
        if (this.viewModel.roomInfo.blackPlayerId == this.viewModel.playerId) {
            return PlayerColor.Black;
        }
        else if (this.viewModel.roomInfo.whitePlayerId == this.viewModel.playerId) {
            return PlayerColor.White;
        }
        else {
            return null;
        }
    }

    get allowedRows() {
        if (this.side() == PlayerColor.White) return [0, 5];
        if (this.side() == PlayerColor.Black) return [2, 7];
        return [-1, -1];
    }

    get sideText(): string {
        if (this.side() == PlayerColor.Black) {
            return "Your piece: @";
        } else if (this.side() == PlayerColor.White) {
            return "Your piece: O, the board is rotated 180° for you";
        }
        else {
            return "";
        }
    }

    get myPiecesCount(): number {
        if (this.side() == PlayerColor.White) {
            return this.viewModel.sessionInfo.whitePiece;
        } else if (this.side() == PlayerColor.Black) {
            return this.viewModel.sessionInfo.blackPiece;
        } else {
            return 0;
        }
    }

    get oppoPiecesCount(): number {
        if (this.side() == PlayerColor.White) {
            return this.viewModel.sessionInfo.blackPiece;
        } else if (this.side() == PlayerColor.Black) {
            return this.viewModel.sessionInfo.whitePiece;
        } else {
            return 0;
        }
    }

    get playerColor(): string {
        if (this.side() == PlayerColor.Black) {
            return Board.CELL_BLACK;
        }
        else {
            return Board.CELL_WHITE;
        }
    }
    get theMode(): PlayBoardMode {
        console.log('side=', this.side(), 'turn=', this.viewModel.sessionInfo.turn);
        if (this.hasWinner) return PlayBoardMode.ViewOnly;
        if (this.viewModel.sessionInfo.phase == GamePhase.Placing && this.viewModel.sessionInfo.turn == this.side()) {
            return PlayBoardMode.SelectForPlacing;
        } else if (this.viewModel.sessionInfo.phase == GamePhase.Moving && this.viewModel.sessionInfo.turn == this.side()) {
            return PlayBoardMode.SelectForMoving;
        } else {
            return PlayBoardMode.ViewOnly;
        }
    }

    get showButton(): boolean {
        if (this.theMode != PlayBoardMode.ViewOnly) {
            if (this.boardOutput != null) {
                if (this.boardOutput.newX != null || this.boardOutput.fromX != null) return true;
            } else {
                return false;
            }
        }
        return false;
    }

    get previewMove() {
        if (this.boardOutput) {
            if (this.viewModel.sessionInfo.phase == GamePhase.Placing) {
                return `Placing a new piece at (${this.boardOutput.newX}, ${this.boardOutput.newY})?`;
            } else if (this.viewModel.sessionInfo.phase == GamePhase.Moving) {
                return `Moving the piece from (${this.boardOutput.fromX}, ${this.boardOutput.fromY}) to (${this.boardOutput.toX},${this.boardOutput.toY})?`;
            }
        } else {
            return "";
        }
    }

    onSubmit() {
        if (this.boardOutput) {
            console.log('To submit move:', this.boardOutput);
            // var submit = 
            if (this.viewModel.sessionInfo.phase == GamePhase.Placing) {
                Socket.placePiece(this.boardOutput.newX, this.boardOutput.newY);
            } else if (this.viewModel.sessionInfo.phase == GamePhase.Moving) {
                Socket.movePiece(this.boardOutput.fromX, this.boardOutput.fromY,
                    this.boardOutput.toX, this.boardOutput.toY);
            }

        }

    }

    onPass() {
        Socket.pass();
    }

    onQuit() {
        if (confirm("Are you sure you want to quit? Game will end if you quit.")) {
            Socket.leaveRoom();
        }
    }

    get lastMove(): PlayerAction {
        if (this.viewModel.sessionInfo.listOfMoves.length > 0) {
            return this.viewModel.sessionInfo.listOfMoves[this.viewModel.sessionInfo.listOfMoves.length - 1][2];
        }
        return null;
    }

    get listOfMoves(): Array<any> {
        if (!this.viewModel.sessionInfo.listOfMoves) return [];
        return this.viewModel.sessionInfo.listOfMoves.map(
            (move, i) => {
                var playerName = move[1] == PlayerColor.Black ? this.viewModel.roomInfo.blackPlayerName : this.viewModel.roomInfo.whitePlayerName;
                var moveType = move[2].type;
                if (moveType == PlayerActionType.MakeMove) {
                    let act = move[2] as PlayerMoveAction;
                    return [i, `Player ${playerName} moved (${act.fromX},${act.fromY}) to (${act.toX},${act.toY}).`];
                } else if (moveType == PlayerActionType.Place) {
                    let act = move[2] as PlayerPlaceAction;
                    return [i, `Player ${playerName} placed a piece at (${act.newX},${act.newY}).`];
                } else {
                    return [i, `Player ${playerName} chose to pass.`];
                }
            }
        )
    }

    get hasWinner(): boolean {
        return this.viewModel.sessionInfo.winner != null;
    }

    get hasEnded(): boolean {
        return this.viewModel.sessionInfo.quitter == true;
    }

    get winnerName(): string {
        if (this.viewModel.sessionInfo.winner == PlayerColor.Black) {
            return this.viewModel.roomInfo.blackPlayerName;
        } else if (this.viewModel.sessionInfo.winner == PlayerColor.White) {
            return this.viewModel.roomInfo.whitePlayerName;
        }
    }

    onReturnClicked() {
        Socket.newSession();
    }

    get myTurn(): boolean {
        if (this.hasWinner) return false;
        if (this.viewModel.sessionInfo.turn == PlayerColor.Black && this.viewModel.roomInfo.blackPlayerId == this.viewModel.playerId)
            return true;
        if (this.viewModel.sessionInfo.turn == PlayerColor.White && this.viewModel.roomInfo.whitePlayerId == this.viewModel.playerId)
            return true;
        return false;
    }
}

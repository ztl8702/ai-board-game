import Vue from 'vue';
import Component from "vue-class-component";
import { Prop } from "vue-property-decorator";
import { Socket } from '../utils';
import { PlayBoard, PlayBoardMode, PlacingProgressBar, WhosTurn } from "../components";
import { ClientViewModel } from '../models/ClientViewModel';
import { GamePhase, PlayerColor, PlayerActionType, Player, Board, PlayerMoveAction, PlayerPlaceAction } from '../../src/logic';
declare var $ : any;


@Component({
    name: 'board-page',
    template: `
    <div class="ui grid stackable doubling container">
        <div class="two column row">
            <div class="seven wide column">
                <play-board 
                    v-bind:mode="theMode" 
                    v-bind:board="viewModel.board" 
                    v-bind:playerColor="playerColor" 
                    v-model="boardOutput"
                    v-bind:rotate="shouldRotateBoard" />
            </div>
            <div class="nine wide column">
                <whos-turn v-bind:yours="myTurn" v-bind:oppo="!myTurn && !hasWinner" />
                <placing-progress-bar 
                    v-bind:progress="10" 
                    label="Placing Phase" 
                    v-bind:total="24"/>
                <h1 v-if="hasWinner==false">Playing {{roomId}} - {{getPhaseString()}} Round #{{viewModel.sessionInfo.round}}</h1>
                <h1 v-if="hasWinner" style="color:red">Winner is {{winnerName}}! <button @click="onReturnClicked">Return to room</button></h1>
                <div v-if="myTurn">
                    <button @click="onSubmit" class="ui blue button" v-if="showButton">Submit (Enter)</button>
                    <button @click="onPass" class="ui yellow button" v-if="isMoving" >Pass</button>
                </div>
            </div>
        </div>
        <div class="one column row">
            <div class="column">
                <table class="ui single line table">
                    <thead>
                        <tr>
                        <th>#</th>
                        <th>Move</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr v-for="(move,index) in listOfMoves.slice().reverse()">
                        <td>{{index}}</td>
                        <td>{{move}}</td>
                        </tr>
                        
                    </tbody>
                </table>
            </div>
        </div>
    </div>`,
    components: { PlayBoard, PlacingProgressBar, WhosTurn }
})
export class BoardPage extends Vue {
    @Prop()
    viewModel: ClientViewModel;

    data = {
        'boardOutput': null
    };

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

    get shouldRotateBoard() :boolean {
        return this.side() == PlayerColor.White;
    }

    get isPlacing() : boolean{
        try {
            if (this.viewModel.sessionInfo.phase == GamePhase.Placing) {
                return true;
            } 
        } catch {

        }
        return false;
    }

    get isMoving() : boolean {
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
                return true;
            } else {
                return false;
            }
        }
        return false;
    }

    onSubmit() {
        console.log('To submit move:', this.boardOutput);
        // var submit = 
        if (this.viewModel.sessionInfo.phase == GamePhase.Placing) {
            Socket.placePiece(this.boardOutput.newX, this.boardOutput.newY);
        } else if (this.viewModel.sessionInfo.phase == GamePhase.Moving) {
            Socket.movePiece(this.boardOutput.fromX, this.boardOutput.fromY,
                this.boardOutput.toX, this.boardOutput.toY);
        }

    }

    onPass() {
        Socket.pass();
    }

    get listOfMoves(): Array<string> {
        if (!this.viewModel.sessionInfo.listOfMoves) return [];
        return this.viewModel.sessionInfo.listOfMoves.map(
            (move) => {
                var playerName = move[1] == PlayerColor.Black ? this.viewModel.roomInfo.blackPlayerName : this.viewModel.roomInfo.whitePlayerName;
                var moveType = move[2].type;
                if (moveType==PlayerActionType.MakeMove) {
                    let act = move[2] as PlayerMoveAction;
                    return `Player ${playerName} moved (${act.fromX},${act.fromY}) to (${act.toX},${act.toY}).`
                } else {
                    let act = move[2] as PlayerPlaceAction;
                    return `Player ${playerName} placed a piece at (${act.newX},${act.newY}).`
                }
            }
        )
    }

    get hasWinner() : boolean {
        return this.viewModel.sessionInfo.winner != null;
    }

    get winnerName() : string{
        if (this.viewModel.sessionInfo.winner == PlayerColor.Black) {
            return this.viewModel.roomInfo.blackPlayerName;
        } else if (this.viewModel.sessionInfo.winner == PlayerColor.White) {
            return this.viewModel.roomInfo.whitePlayerName;
        }
    }

    onReturnClicked() {
        Socket.newSession();
    }

    get myTurn() : boolean {
        if (this.hasWinner) return false;
        if (this.viewModel.sessionInfo.turn == PlayerColor.Black && this.viewModel.roomInfo.blackPlayerId == this.viewModel.playerId)
            return true;
        if (this.viewModel.sessionInfo.turn == PlayerColor.White && this.viewModel.roomInfo.whitePlayerId == this.viewModel.playerId)
            return true;
        return false;
    }
}

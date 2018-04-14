import Vue from 'vue';
import Component from "vue-class-component";
import { Prop } from "vue-property-decorator";
import { Socket } from '../utils';
import { PlayBoard, PlayBoardMode } from "./PlayBoard";
import { ClientViewModel } from '../models/ClientViewModel';
import { GamePhase, PlayerColor, PlayerActionType, Player, Board, PlayerMoveAction, PlayerPlaceAction } from '../../src/logic';



@Component({
    name: 'board-page',
    template: `
    <div>
        <h1 v-if="hasWinner==false">Playing {{roomId}} - {{getPhaseString()}} Round #{{viewModel.sessionInfo.round}}</h1>
        <h2 v-if="myTurn">Your turn</h2>
        <h1 v-if="hasWinner" style="color:red">Winner is {{winnerName}}! <button @click="onReturnClicked">Return to room</button></h1>
        <play-board v-bind:mode="theMode" v-bind:board="viewModel.board" v-bind:playerColor="playerColor" v-model="boardOutput"/>
        <button @click="onSubmit" v-if="showButton">Submit</button>
        <div>
            <ul>
                <li v-for="move in listOfMoves">{{move}}</li>
            </ul>
        </div>
    </div>`,
    components: { PlayBoard }
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

    get listOfMoves(): Array<string> {
        if (!this.viewModel.sessionInfo.listOfMoves) return [];
        return this.viewModel.sessionInfo.listOfMoves.map(
            (move) => {
                var playerName = move[1] == PlayerColor.Black ? this.viewModel.roomInfo.blackPlayerName : this.viewModel.roomInfo.whitePlayerName;
                var moveType = move[2].type;
                if (moveType==PlayerActionType.MakeMove) {
                    let act = move[2] as PlayerMoveAction;
                    return `Player ${playerName} moved (${act.fromY},${act.fromY}) to (${act.toX},${act.toY}).`
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

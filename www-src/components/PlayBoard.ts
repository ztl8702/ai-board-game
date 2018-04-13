import Vue from 'vue';
import Component from "vue-class-component";
import { BoardCell, HighlightStyle } from './BoardCell';
import { Board } from "../../src/logic";

@Component({
    name: 'play-board',
    template: `<table class="board">
    <tr v-for="row in rows">
        <board-cell v-for="col in row.cols" 
        v-bind:x="col.x"
        v-bind:y="col.y"
        v-bind:pieceColor="getPieceColor(col.x, col.y)"
        v-bind:highlight="getHighlightStyle(col.x, col.y)"
        v-on:clicked="cellClicked"
        />
    </tr>
    </table>`,
    components: { BoardCell }
})
export class PlayBoard extends Vue {

    selectedCell: any | null = null;
    targetCell: any | null = null;
    availableCells: Array<[number, number]> = [];
    board: Board = new Board();
    private selectionState: PlayBoardSelectionState = PlayBoardSelectionState.NoSelection;

    constructor() {
        super();
        this.board.set(1, 1, Board.CELL_BLACK);
        this.board.set(2, 2, Board.CELL_WHITE);
    }

    get rows(): any {
        var result = [];
        for (var y = 0; y <= 7; ++y) {
            var currentRow = { 'cols': [] };
            for (var x = 0; x <= 7; ++x) {
                currentRow['cols'].push({
                    'x': x,
                    'y': y
                });
            }
            result.push(currentRow);
        }
        return result;
    }

    getHighlightStyle(x: number, y: number): HighlightStyle {
        switch (this.selectionState) {
            case PlayBoardSelectionState.NoSelection:
                return HighlightStyle.None;
            case PlayBoardSelectionState.SelectedOne:
                if ([x, y].toString() == this.selectedCell.toString()) {
                    return HighlightStyle.Selected;
                } else {
                    var hints = this.board.getAvailableMoves(this.selectedCell[0], this.selectedCell[1]);
                    if (hints.map(x => x.toString()).indexOf([x, y].toString()) != -1) {
                        return HighlightStyle.Hint;
                    }
                }

                return HighlightStyle.None;
            case PlayBoardSelectionState.SelectedTarget:
                if ([x, y].toString() == this.selectedCell.toString()) {
                    return HighlightStyle.Selected;
                }
                if (this.targetCell != null && [x, y].toString() == this.targetCell.toString()) {
                    return HighlightStyle.Target;
                }
                return HighlightStyle.None;

        }
    }

    getPieceColor(x, y): string {
        return this.board.get(x, y);
    }

    cellClicked(x, y) {
        console.log(`PlayBoard: cell clicked (${x},${y})`);
        switch (this.selectionState) {
            case PlayBoardSelectionState.NoSelection:
                if (this.board.get(x, y) == Board.CELL_BLACK || this.board.get(x, y) == Board.CELL_WHITE) {
                    this.selectedCell = [x, y];
                    this.selectionState = PlayBoardSelectionState.SelectedOne;
                    this.availableCells = this.board.getAvailableMoves(x, y);
                }
                break;
            case PlayBoardSelectionState.SelectedOne:
                if (this.availableCells.map(x => x.toString()).indexOf([x, y].toString()) != -1) {
                    this.targetCell = [x, y];
                    this.selectionState = PlayBoardSelectionState.SelectedTarget;
                } else if (this.board.get(x, y) == Board.CELL_BLACK || this.board.get(x, y) == Board.CELL_WHITE) {
                    this.selectedCell = [x, y];
                    this.availableCells = this.board.getAvailableMoves(x, y);
                } else {
                    this.selectedCell = null;
                    this.availableCells = [];
                    this.selectionState = PlayBoardSelectionState.NoSelection;
                }
                break;
            case PlayBoardSelectionState.SelectedTarget:
                if (this.targetCell.toString() == [x, y].toString()) {
                    this.targetCell = null;
                    this.selectionState = PlayBoardSelectionState.SelectedOne;
                } else if (this.availableCells.map(x => x.toString()).indexOf([x, y].toString()) != -1) {
                    this.targetCell = [x, y];
                } else if (this.board.get(x, y) == Board.CELL_BLACK || this.board.get(x, y) == Board.CELL_WHITE) {
                    this.targetCell = null;
                    this.selectedCell = [x, y];
                    this.availableCells = this.board.getAvailableMoves(x, y);
                    this.selectionState = PlayBoardSelectionState.SelectedOne;
                } else {
                    this.selectedCell = null;
                    this.availableCells = [];
                    this.targetCell = null;
                    this.selectionState = PlayBoardSelectionState.NoSelection;
                }
                break;
        }

        console.log(this.selectionState, this.selectedCell, this.availableCells, this.targetCell);
        this.$forceUpdate();
    }
}

enum PlayBoardSelectionState {
    NoSelection,
    SelectedOne,
    SelectedTarget,
}
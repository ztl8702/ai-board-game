import Vue from 'vue';
import Component from "vue-class-component";
import { BoardCell, HighlightStyle, IndexCell } from './';
import { Board } from "../../src/logic";
import { Prop } from "vue-property-decorator";
import { Socket } from '../utils';


export enum PlayBoardMode {
    ViewOnly,
    SelectForPlacing,
    SelectForMoving
}


@Component({
    name: 'play-board',
    template: `<table class="board">
    <tr>
        <index-cell />
        <index-cell v-for="col in rows[0].cols" v-bind:displayText="col.x" /> 
    </tr>
    <tr v-for="row in rows">
        <index-cell v-bind:displayText="row.id" />
        <board-cell v-for="col in row.cols" 
        v-bind:x="col.x"
        v-bind:y="col.y"
        v-bind:pieceColor="getPieceColor(col.x, col.y)"
        v-bind:highlight="getHighlightStyle(col.x, col.y)"
        v-on:clicked="cellClicked"
        />
    </tr>
    </table>`,
    components: { BoardCell, IndexCell }
})
export class PlayBoard extends Vue {

    selectedCell: any | null = null;
    targetCell: any | null = null;
    availableCells: Array<[number, number]> = [];
    @Prop({})
    board: Board = new Board();
    private selectionState: PlayBoardSelectionState = PlayBoardSelectionState.NoSelection;

    constructor() {
        super();
        this.board.set(1, 1, Board.CELL_BLACK);
        this.board.set(2, 2, Board.CELL_WHITE);
    }

    @Prop({})
    mode: PlayBoardMode = PlayBoardMode.ViewOnly;
    @Prop({})
    playerColor: string;
    watch = {
        'mode': (val) => {
            if (val == PlayBoardMode.ViewOnly) {
                this.selectionState = PlayBoardSelectionState.NoSelection;
                this.selectedCell = null;
                this.targetCell = null;
                this.availableCells = [];
            }
            //this.mode = val;
        }
    }
    @Prop({})
    value: any;

    @Prop({})
    rotate: boolean = false;

    updated() {
        console.log('PlayBoard updated.')
        if (this.mode == PlayBoardMode.ViewOnly) {
            this.selectionState = PlayBoardSelectionState.NoSelection;
            this.selectedCell = null;
            this.targetCell = null;
            this.availableCells = [];
        }
    }

    get movingOutput() {
        if (this.mode == PlayBoardMode.SelectForMoving && this.selectionState == PlayBoardSelectionState.SelectedTarget) {
            return {
                fromX: this.selectedCell[0],
                fromY: this.selectedCell[1],
                toX: this.targetCell[0],
                toY: this.targetCell[1]
            }

        } else {
            return null;
        }
    }

    get placingOutput() {
        if (this.mode == PlayBoardMode.SelectForPlacing && this.selectionState == PlayBoardSelectionState.SelectedTarget) {
            return {
                newX: this.targetCell[0],
                newY: this.targetCell[1]
            }

        } else {
            return null;
        }
    }

    private updateOutput() {
        if (this.mode == PlayBoardMode.SelectForMoving) {
            this.$emit('input', this.movingOutput);
        } else if (this.mode == PlayBoardMode.SelectForPlacing) {
            this.$emit('input', this.placingOutput);
        } else {
            this.$emit('input', null);
        }
    }

    get rows(): any {
        var result = [];
        if (!this.rotate) {
            for (var y = 0; y <= 7; ++y) {
                var currentRow = { 'id': y, 'cols': [] };
                for (var x = 0; x <= 7; ++x) {
                    currentRow['cols'].push({
                        'x': x,
                        'y': y
                    });
                }
                result.push(currentRow);
            }
        } else {
            for (var y = 7; y >= 0; --y) {
                var currentRow = { 'id': y, 'cols': [] };
                for (var x = 7; x >= 0; --x) {
                    currentRow['cols'].push({
                        'x': x,
                        'y': y
                    });
                }
                result.push(currentRow);
            }
        }
        return result;
    }

    getHighlightStyle(x: number, y: number): HighlightStyle {
        switch (this.mode) {
            case PlayBoardMode.ViewOnly:
                return HighlightStyle.None;
            case PlayBoardMode.SelectForMoving:
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
                break;
            case PlayBoardMode.SelectForPlacing:
                switch (this.selectionState) {
                    case PlayBoardSelectionState.NoSelection:
                        return HighlightStyle.None;
                    case PlayBoardSelectionState.SelectedTarget:
                        if ([x, y].toString() == this.targetCell.toString()) {
                            return HighlightStyle.Target;
                        }
                        return HighlightStyle.None;
                }
        }
    }

    getPieceColor(x, y): string {
        return this.board.get(x, y);
    }

    cellClicked(x, y) {
        console.log(`PlayBoard: cell clicked (${x},${y})`);
        switch (this.mode) {
            case PlayBoardMode.ViewOnly:
                this.selectedCell = null;
                this.targetCell = null;
                this.availableCells = [];
                this.selectionState = PlayBoardSelectionState.NoSelection;
                break;
            case PlayBoardMode.SelectForMoving:
                switch (this.selectionState) {
                    case PlayBoardSelectionState.NoSelection:
                        if (this.board.get(x, y) == this.playerColor) {
                            this.selectedCell = [x, y];
                            this.selectionState = PlayBoardSelectionState.SelectedOne;
                            this.availableCells = this.board.getAvailableMoves(x, y);
                        }
                        break;
                    case PlayBoardSelectionState.SelectedOne:
                        if (this.availableCells.map(x => x.toString()).indexOf([x, y].toString()) != -1) {
                            this.targetCell = [x, y];
                            this.selectionState = PlayBoardSelectionState.SelectedTarget;
                        } else if (this.board.get(x, y) == this.playerColor) {
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
                        } else if (this.board.get(x, y) == this.playerColor) {
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
                break;
            case PlayBoardMode.SelectForPlacing:
                switch (this.selectionState) {
                    case PlayBoardSelectionState.NoSelection:
                        if (this.board.isEmpty(x, y)) {
                            this.targetCell = [x, y];
                            this.selectionState = PlayBoardSelectionState.SelectedTarget;
                        }
                        break;
                    case PlayBoardSelectionState.SelectedTarget:
                        if (this.board.isEmpty(x, y) && this.targetCell.toString() != [x, y].toString()) {
                            this.targetCell = [x, y];
                        } else {
                            this.targetCell = null;
                            this.selectionState = PlayBoardSelectionState.NoSelection;
                        }
                        break;
                }
                break;
        }


        console.log(this.selectionState, this.selectedCell, this.availableCells, this.targetCell);
        this.updateOutput();
        this.$forceUpdate();
    }
}

enum PlayBoardSelectionState {
    NoSelection,
    SelectedOne,
    SelectedTarget,
}


import Vue from 'vue';
import Component from "vue-class-component";
import { Prop, Watch } from "vue-property-decorator";
import VueKonva from "vue-konva";
import { CanvasCell } from "./CanvasCell";
import { CanvasIndexCell } from "./CanvasIndexCell";
import { HighlightStyle, PlayBoardMode, PlayBoardSelectionState } from '.';
import { Board, PlayerAction, PlayerMoveAction, PlayerActionType, PlayerPlaceAction } from '../../src/logic';

Vue.use(VueKonva);

@Component({
    name: 'canvas-board',
    template: ` 
    <v-stage :config="configStage">
        <v-layer ref="layer2">
            <v-rect ref="zone" v-if="showZone" :config="configZone" />
        </v-layer>
        <v-layer ref="layer">
        
            <canvas-index-cell :left="0" :top="0" />
            <canvas-index-cell v-for="(col,i) in rows.rows[0].cols" :left="getX(i+1)" :top="0" v-bind:displayText="col.x.toString()" /> 
            <canvas-index-cell v-for="(row,i) in rows.rows" :left="0" :top="getY(i+1)" v-bind:displayText="row.id.toString()" /> 

            <canvas-cell v-for="cell in rows.meshed" 
                :x="cell.x"
                :y="cell.y"
                :top="getY(cell.j + 1)"
                :left="getX(cell.i + 1)"
                :parentRefs="$refs"
                v-bind:pieceColor="getPieceColor(cell.x, cell.y)"
                v-bind:highlight="getHighlightStyle(cell.x, cell.y)"
                v-bind:highlightLast="getHighlightLast(cell.x, cell.y)"
                v-on:clicked="cellClicked"
                />
        </v-layer>

    </v-stage>`,
    components: { CanvasCell, CanvasIndexCell }
})
export class CanvasBoard extends Vue {

    public static readonly CELL_SIZE = 40;
    public static readonly CELL_PADDING = 5;
    public static readonly BG_NORMAL = "#f5f5f5";
    public static readonly BG_DEAD = "gray";
    public static readonly BG_CORNER = "#efefef";
    public static readonly BG_HINT = "#ffee7f";
    public static readonly BG_SELECTED = "lightblue";

    @Prop({ default: true }) rotate: boolean = true;
    selectedCell: any | null = null;
    targetCell: any | null = null;
    availableCells: Array<[number, number]> = [];
    @Prop({}) board: Board = new Board();
    private selectionState: PlayBoardSelectionState = PlayBoardSelectionState.NoSelection;
    @Prop({}) mode: PlayBoardMode = PlayBoardMode.ViewOnly;
    @Prop({}) playerColor: string;

    @Prop({}) allowedRowStart: number = null;
    @Prop({}) allowedRowEnd: number = null;
    @Prop({}) lastMove: PlayerAction = null;
    @Prop({}) value: any;

    constructor() {
        super();
        this.board.set(1, 1, Board.CELL_BLACK);
        this.board.set(2, 2, Board.CELL_WHITE);
    }

    get showZone() {
        return this.allowedRowStart >= 0 && this.mode == PlayBoardMode.SelectForPlacing;
    }

    updated() {
        console.log('PlayBoard updated.')
        if (this.mode == PlayBoardMode.ViewOnly) {
            this.selectionState = PlayBoardSelectionState.NoSelection;
            this.selectedCell = null;
            this.targetCell = null;
            this.availableCells = [];
        }
    }

    data() {
        return {
            configStage: {
                width: CanvasBoard.CELL_SIZE * 9 + CanvasBoard.CELL_PADDING * 9,
                height: CanvasBoard.CELL_SIZE * 9 + CanvasBoard.CELL_PADDING * 9
            }
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

    getX(col) {
        return col * (CanvasBoard.CELL_SIZE + CanvasBoard.CELL_PADDING);
    }


    getY(row) {
        return row * (CanvasBoard.CELL_SIZE + CanvasBoard.CELL_PADDING);
    }

    configRect(row, col) {
        return {
            x: col * (CanvasBoard.CELL_SIZE + CanvasBoard.CELL_PADDING),
            y: row * (CanvasBoard.CELL_SIZE + CanvasBoard.CELL_PADDING),
            width: CanvasBoard.CELL_SIZE,
            height: CanvasBoard.CELL_SIZE,
            fill: CanvasBoard.BG_NORMAL
        }
    }

    get configZone() {
        return {
            x: 0,
            y: this.getY(3),
            fill: 'lightgreen',
            width: CanvasBoard.CELL_SIZE * 9 + CanvasBoard.CELL_PADDING * 9,
            height: CanvasBoard.CELL_SIZE * 6 + CanvasBoard.CELL_PADDING * 6,
            opacity: 0.8
        }
    }

    get rows(): any {
        var result = { 'rows': [], 'meshed': [] }
        if (!this.rotate) {
            for (var y = 0; y <= 7; ++y) {
                var currentRow = { 'id': y, 'cols': [] };
                for (var x = 0; x <= 7; ++x) {
                    currentRow['cols'].push({
                        'x': x,
                        'y': y
                    });
                    result.meshed.push({ 'x': x, 'y': y, 'i': x, 'j': y });
                }
                result.rows.push(currentRow);
            }
        } else {
            for (var y = 7, j = 0; y >= 0; --y, ++j) {
                var currentRow = { 'id': y, 'cols': [] };
                for (var x = 7, i = 0; x >= 0; --x, ++i) {
                    currentRow['cols'].push({
                        'x': x,
                        'y': y
                    });
                    result.meshed.push({ 'x': x, 'y': y, 'i': i, 'j': j });

                }
                result.rows.push(currentRow);
            }
        }
        return result;
    }

    getPieceColor(x, y): string {
        return this.board.get(x, y);
    }

    getHighlightLast(x: number, y: number) {
        if (this.lastMove != null) {
            if (this.lastMove.type == PlayerActionType.Place) {
                if (x == (this.lastMove as PlayerPlaceAction).newX
                    && y == (this.lastMove as PlayerPlaceAction).newY) {
                    return HighlightStyle.LastMove1;
                }
            } else if (this.lastMove.type == PlayerActionType.MakeMove) {
                if (x == (this.lastMove as PlayerMoveAction).fromX
                    && y == (this.lastMove as PlayerMoveAction).fromY) {
                    return HighlightStyle.LastMove1;
                }
                if (x == (this.lastMove as PlayerMoveAction).toX
                    && y == (this.lastMove as PlayerMoveAction).toY) {
                    return HighlightStyle.LastMove2;
                }
            }
        }
        return HighlightStyle.None;
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

    cellClicked(x, y) {
        console.log(`CanvasBoard: cell clicked (${x},${y})`);
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


    @Watch("mode")
    onModeChanged(val) {
        // if (val == PlayBoardMode.ViewOnly) {
        this.selectionState = PlayBoardSelectionState.NoSelection;
        this.selectedCell = null;
        this.targetCell = null;
        this.availableCells = [];
        this.$emit('input', null);
        //} 
        //this.mode = val;
    }

    @Watch("mode")
    @Watch("allowedRowStart") 
    onUpdateZone() {
        try {
            if (this.showZone) {
                (this.$refs.zone as any).getStage().opacity(0.8);
            } else {
                (this.$refs.zone as any).getStage().opacity(0);
                
            }
            (this.$refs.layer2 as any).getStage().draw();

        } catch {
            
        }
    }

}
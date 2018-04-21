import Vue from 'vue';
import Component from "vue-class-component";
import { Prop, Watch } from "vue-property-decorator";
import VueKonva from "vue-konva";
import { CanvasBoard } from './CanvasBoard';
import { Board } from '../../src/logic';
import { HighlightStyle } from '.';

declare var Konva : any;
Vue.use(VueKonva);

@Component({
    name: 'canvas-cell',
    template: ` 
    <v-group :config="configGroup" @click="onClick">
        <v-rect ref="rect" :config="configRect" />
        <v-text :config="configText" />
    </v-group>`,
})
export class CanvasCell extends Vue {

    @Prop()
    left: number = 0;
    @Prop()
    top: number = 0;

    @Prop()
    x: number;
    @Prop()
    y: number;

    @Prop()
    pieceColor: string = Board.CELL_EMPTY;

    @Prop()
    highlight: HighlightStyle = HighlightStyle.None;

    @Prop()
    highlightLast: HighlightStyle = HighlightStyle.None;

    @Prop()
    parentRefs: any= null;

    get isBlack(): boolean {
        return (this.pieceColor == Board.CELL_BLACK);
    }

    get isWhite(): boolean {
        return (this.pieceColor == Board.CELL_WHITE);
    }

    get isSelected(): boolean {
        return (this.pieceColor != Board.CELL_DEAD && this.pieceColor != Board.CELL_CORNER && this.highlight == HighlightStyle.Selected);
    }

    get isHint(): boolean {
        return (this.pieceColor != Board.CELL_DEAD && this.pieceColor != Board.CELL_CORNER && this.highlight == HighlightStyle.Hint);
    }

    get isTarget(): boolean {
        return (this.pieceColor != Board.CELL_DEAD && this.pieceColor != Board.CELL_CORNER && this.highlight == HighlightStyle.Target);
    }


    get isDead(): boolean {
        return this.pieceColor == Board.CELL_DEAD;
    }

    get isCorner(): boolean {
        return this.pieceColor == Board.CELL_CORNER;
    }

    get isLastMove1(): boolean {
        return this.highlightLast == HighlightStyle.LastMove1;
    }

    get isLastMove2(): boolean {
        return this.highlightLast == HighlightStyle.LastMove2;
    }

    get displayText(): string {
        switch (this.pieceColor) {
            case Board.CELL_BLACK:
                return '@';
            case Board.CELL_WHITE:
                return 'O';
            case Board.CELL_CORNER:
                return 'X';
            default:
                return ' ';
        }
    }

    get configGroup() {
        return {
            x: this.left,
            y: this.top,
            width: CanvasBoard.CELL_SIZE,
            height: CanvasBoard.CELL_SIZE
        }
    }

    get bgColor() {
        var bgColor = CanvasBoard.BG_NORMAL;
        if (this.isSelected) {
            bgColor = CanvasBoard.BG_SELECTED;
        } else if (this.isHint || this.isTarget) {
            bgColor = CanvasBoard.BG_HINT;
        } else if (this.isDead) {
            bgColor = CanvasBoard.BG_DEAD;
        } else if (this.isCorner) {
            bgColor = CanvasBoard.BG_CORNER;
        }
        return bgColor
    }

    get stroke() {
        if (this.isLastMove1) {
            return {
                'stroke':CanvasBoard.BG_SELECTED,
                'strokeWidth': 3
            }
        }
        if (this.isLastMove2) {
            return {
                'stroke':CanvasBoard.BG_HINT,
                'strokeWidth': 3
            }
        }
        return {
            'stroke':'',
            'strokeWidth':0
        }
    }
    get configRect() {
        return {
            width: CanvasBoard.CELL_SIZE,
            height: CanvasBoard.CELL_SIZE,
            fill: this.bgColor,
            stroke: this.stroke.stroke,
            strokeWidth: this.stroke.strokeWidth
        }
    }

    get configText() {
        return {
            text: this.displayText,
            x: 5,
            y: 5,
            fill: "black",
            fontSize: 30,
            fontFamily: 'sans-serif',
            fontStyle: 'bold',
            width: CanvasBoard.CELL_SIZE,
            height: CanvasBoard.CELL_SIZE
        }
    }

    blinkingAnim = null;

    @Watch("highlight")
    onHighlightChange() {
        (this.$refs.rect as any).getStage().fill(this.bgColor);
        (this.$refs.rect as any).getStage().stroke(this.stroke.stroke);
        (this.$refs.rect as any).getStage().strokeWidth(this.stroke.strokeWidth);
        this.$forceUpdate();
        this.parentRefs.layer.getStage().draw();
        if (this.isTarget) {
            this.blinkingAnim = new Konva.Animation( (frame) =>{
                var op = (Math.sin(frame.time*2*Math.PI/1000) + 1)/2;
               // console.log(this.$refs.rect);
                (this.$refs.rect as any).getStage().opacity(op);
                //console.log(op);
            }, (this.parentRefs.layer as any).getStage());
            this.blinkingAnim.start();
        } else {
            if (this.blinkingAnim) {
                this.blinkingAnim.stop();
                this.blinkingAnim = null;
                (this.$refs.rect as any).getStage().opacity(1);
            }
        }
    }

    @Watch("highlightLast") 
    @Watch("pieceColor")
    onHighlightLastChange() {
        (this.$refs.rect as any).getStage().fill(this.bgColor);
        (this.$refs.rect as any).getStage().stroke(this.stroke.stroke);
        (this.$refs.rect as any).getStage().strokeWidth(this.stroke.strokeWidth);
        this.$forceUpdate();
        this.parentRefs.layer.getStage().draw();
    }

    private onClick(): void {
        console.log(`Cell (${this.x},${this.y}) clicked.`);
        this.$emit('clicked', this.x, this.y);
    }

}
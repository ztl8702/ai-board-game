import Vue from 'vue';
import Component from "vue-class-component";
import { Prop } from "vue-property-decorator";
import { Board } from "../../src/logic";


export enum HighlightStyle {
    None,
    Selected,
    Hint,
    Target
}

@Component({
    name:'board-cell',
    template: `
        <div 
            class="board-cell" 
            v-bind:class="{ pblack: isBlack, pwhite: isWhite, selected: isSelected, hint: isHint, target: isTarget, dead: isDead, corner:isCorner}" 
            @click="onClick"><div class="board-cell__inner">{{ displayText }}</div></div>`,
})
export class BoardCell extends Vue {

    @Prop()
    x: number;
    @Prop()
    y: number;

    @Prop({ default: Board.CELL_EMPTY })
    pieceColor: string;

    @Prop({ default: HighlightStyle.None })
    highlight: HighlightStyle;

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

    get isCorner(): boolean{
        return this.pieceColor == Board.CELL_CORNER;
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

    private onClick(): void {
        console.log(`Cell (${this.x},${this.y}) clicked.`);
        this.$emit('clicked',this.x,this.y);
    }


}

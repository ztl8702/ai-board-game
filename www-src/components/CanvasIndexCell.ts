import Vue from 'vue';
import Component from "vue-class-component";
import { Prop, Watch } from "vue-property-decorator";
import VueKonva from "vue-konva";
import { CanvasBoard } from './CanvasBoard';
import { Board } from '../../src/logic';
import { HighlightStyle } from '.';

declare var Konva: any;
Vue.use(VueKonva);

@Component({
    name: 'canvas-index-cell',
    template: ` 
    <v-group :config="configGroup">
        <v-rect ref="rect" :config="configRect" />
        <v-text :config="configText" />
    </v-group>`,
})
export class CanvasIndexCell extends Vue {

    @Prop()
    left: number = 0;
    @Prop()
    top: number = 0;

    @Prop()
    displayText: string = "";

    get configGroup() {
        return {
            x: this.left,
            y: this.top
        }
    }

    get configRect() {
        var result = {
            width: CanvasBoard.CELL_SIZE,
            height: CanvasBoard.CELL_SIZE,
            fill: 'white'
        }
        return result;
    }

    get configText() {
        return {
            text: this.displayText,
            x: 20,
            y: 12,
            fill: "darkgray",
            fontSize: 15,
            fontFamily: 'sans-serif',
            fontStyle: 'bold',
            width: CanvasBoard.CELL_SIZE,
            height: CanvasBoard.CELL_SIZE
        }
    }


}
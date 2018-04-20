import Vue from 'vue';
import Component from "vue-class-component";
import { Prop, Watch } from "vue-property-decorator";
import { Socket } from '../utils';
import { ProgressBar } from "./";
import { GameSession } from '../../src/logic/index';

@Component({
    name: 'placing-progress-bar',
    template: `
    <div> 
        <progress-bar label="Placing phase" v-bind:total="total" v-bind:progress="progress" />
    </div>
    `,
    components: { ProgressBar }
})
export class PlacingProgressBar extends Vue {

    @Prop({ default: 1 })
    progress: number;

    @Prop({ default: GameSession.NUMBER_OF_PIECES * 2 })
    total: number;

}

import Vue from 'vue';
import Component from "vue-class-component";
import { Prop, Watch } from "vue-property-decorator";
import { Socket } from '../utils';
import { ProgressBar } from "./";
import { GameSession } from '../../src/logic/index';

@Component({
    name: 'moving-progress',
    template: `
    <div>
        <h3>Remaining pieces</h3>
        <progress-bar label="Opponent's pieces" v-bind:progress="oppo" v-bind:isTiny="true" v-bind:total="total"/>
        <progress-bar label="My pieces" v-bind:progress="mine" v-bind:isTiny="true" v-bind:total="total"/>
    </div>
    `,
    components: { ProgressBar }
})
export class MovingProgress extends Vue {

    @Prop({ default: 0 })
    mine: number = 0;

    @Prop({ default: 0 })
    oppo: number = 0;

    @Prop({ default: GameSession.NUMBER_OF_PIECES })
    total: number;

}

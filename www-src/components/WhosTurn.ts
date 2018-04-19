import Vue from 'vue';
import Component from "vue-class-component";
import { Prop } from "vue-property-decorator";
import { Socket } from '../utils';


@Component({
    name: 'whos-turn',
    template: `
    <div>
        <div class="ui big label" v-bind:class="{olive: yours}">
        Your Turn
        </div> 
        <div class="ui big label" v-bind:class="{brown: oppo}">
        Opponent's Turn
        </div>
    </div>
    `,
})
export class WhosTurn extends Vue {


    @Prop() 
    yours: boolean = false;

    @Prop()
    oppo: boolean = false;

    constructor() {
        super();
    }


}

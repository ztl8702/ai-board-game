import Vue from 'vue';
import Component from "vue-class-component";
import { Prop, Watch } from "vue-property-decorator";


declare var $: any;
@Component({
    name: 'progress-bar',
    template: ` 
    <div class="ui indicating progress" v-bind:class="{tiny: isTiny}">
        <div class="bar"></div>
        <div class="label">{{label}} {{progress}} / {{total}}</div>
    </div>`,
})
export class ProgressBar extends Vue {


    @Prop({ default: 50 })
    progress: number = 50;

    @Prop({ default: 100 })
    total: number = 100;

    @Prop()
    label: string = "";

    @Prop()
    isTiny: boolean = false;

    mounted() {
        console.log($(this.$el), $(this.$el).progress);
        window['haha'] = $(this.$el).progress;
        $(this.$el).progress({
            'percent': this.percent
        });
    }

    updated() {

    }

    @Watch("progress")
    @Watch("total")
    private redraw() {
        $(this.$el).progress({
            'percent': this.percent
        });
    }


    beforeDestroy() {
        $(this.$el).progress('destory');
    }

    get percent() {
        return 100 * this.progress / this.total;
    }

    constructor() {
        super();
    }

}
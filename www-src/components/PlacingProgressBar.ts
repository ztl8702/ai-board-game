import Vue from 'vue';
import Component from "vue-class-component";
import { Prop, Watch } from "vue-property-decorator";
import { Socket } from '../utils';

declare var $:any;
@Component({
    name: 'placing-progress-bar',
    template: `
    <div class="ui indicating progress">
        <div class="bar"></div>
        <div class="label">{{label}} {{progress}} / {{total}}</div>
    </div>
    `,
})
export class PlacingProgressBar extends Vue {


    @Prop({ default: 50})
    progress: number = 50;

    @Prop({default :100})
    total: number = 100;

    @Prop()
    label: string = "";

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
        console.log("redraw", this.percent);
        $(this.$el).progress({
            'percent': this.percent 
        });
    }


    beforeDestroy() {
        $(this.$el).progress('destory');
    }

    get percent() {
        return 100* this.progress / this.total;
    }

    constructor() {
        super();
    }


}

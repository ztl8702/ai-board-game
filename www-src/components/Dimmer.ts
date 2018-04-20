import Vue from 'vue';
import Component from "vue-class-component";
import { Prop, Watch } from "vue-property-decorator";


declare var $:any;
@Component({
    name: 'my-dimmer',
    template: ` 
    <div class="ui dimmer">
        <div class="content">
        <h2 class="ui inverted icon header">
            <slot></slot>
        </h2>
        </div>
    </div>`,
})
export class MyDimmer extends Vue {


    mounted() {
        
        $(this.$el).dimmer("show");
    }

    beforeDestroy() {
        $(this.$el).dimmer('destory');
    }


}
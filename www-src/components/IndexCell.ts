import Vue from 'vue';
import Component from "vue-class-component";
import { Prop } from "vue-property-decorator";
import { Board } from "../../src/logic";


@Component({
    name:'index-cell',
    template: `
        <div 
            class="board-cell index" 
        ><div class="board-cell__inner">{{ displayText }}</div></div>`,
})
export class IndexCell extends Vue {
   
    @Prop()
    displayText: string = "";

}

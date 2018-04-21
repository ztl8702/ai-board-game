import Vue from 'vue';
import Component from "vue-class-component";
import { Prop } from "vue-property-decorator";
import { Socket } from '../utils';


@Component({
    name: 'welcome-player-card',
    template: `
    <div class="ui segment">
        <h2 v-if="side=='black'">@ Black player</h2>
        <h2 v-if="side=='white'">O White player</h2>
        <div class="item" v-if="playerName">
            <a class="ui tiny circular image">
                <img src="https://semantic-ui.com/images/wireframe/square-image.png">
            </a>
            <div class="middle aligned content">
                <div class="header">
                {{playerName}}
                </div>
            </div>
        </div>
    </div>
    `,
})
export class WelcomePlayerCard extends Vue {


    @Prop()
    playerName: string;

    @Prop()
    side: string;

}

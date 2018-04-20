import Vue from 'vue';
import Component from "vue-class-component";
import { Prop } from "vue-property-decorator";
import { Socket } from '../utils';


@Component({
    name:'welcome-page',
    template: `
    <div class="ui one column center aligned grid container">
        <div class="column">
            <div class="ui inverted segment center">
                <h3>Hi {{playerName}}</h3>
                <h1>Welcome to WYB Online</h1>
            </div>
            <h2>Create or join a room</h2>
            <div class="ui action input center">
                <input v-model="roomId" placeholder="Enter room name..." type="text"/>
                <button class="ui button" @click="onJoinClicked">Join</button>
            </div>
           <!-- <h2>Leaderboard</h2>-->
           <div style="margin-top:100px;">
           <hr />
           <i>Disclaimer: "Watch Your Back" is designed by the COMP30024 teaching team (lecturer: Sarah Monazam Erfani; head tutor: Matthew Farrugia-Roberts) at the University of Melbourne. This online game is independently implemented by <a href="http://github.com/ztl8702/">Tianlei Zheng</a> and <a href="http://github.com/TTVS/">Terrence Lua</a>. For bugs, <a href="mailto:wybonline@googlegroups.com">send us an email</a>.
           </div>
        </div>
    </div>`,
})
export class WelcomePage extends Vue {
    roomId: string;
    data = {
        'roomId': ''
    }

    @Prop()
    playerName: string;
    constructor() {
        super();
    }

    onJoinClicked() {
        if (this.roomId != '' && this.roomId!=null) {
            this.roomId = this.roomId.substring(0,50); //limit length
            Socket.joinRoom(this.roomId);
        }
    }
}

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
            <h2>Leaderboard</h2>
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

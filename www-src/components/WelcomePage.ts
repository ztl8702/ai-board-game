import Vue from 'vue';
import Component from "vue-class-component";
import { Prop } from "vue-property-decorator";
import { Socket } from '../utils';


@Component({
    name:'welcome-page',
    template: `
    <div>
        <h1>Welcome {{playerName}}</h1>
        <h2>Join Room</h2>
        <input v-model="roomId" />
        <button @click="onJoinClicked">Join</button>
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

import Vue from 'vue';
import Component from "vue-class-component";
import { Prop } from "vue-property-decorator";
import { Socket } from '../utils';


@Component({
    name:'room-page',
    template: `
    <div>
    <h1>Room {{roomId}}<button @click="onLeaveRoom">Leave room</button></h1>
    
        <div>
            Black player: {{viewModel.roomInfo ? viewModel.roomInfo.blackPlayerName : ""}}
        </div>
        <div>
            White player: {{viewModel.roomInfo ? viewModel.roomInfo.whitePlayerName : ""}}
        </div>
        <button @click="onStartClicked">Start Game</button>

    </div>`,
})
export class RoomPage extends Vue {
    @Prop()
    roomId: string;
    @Prop()
    viewModel: any;
    constructor() {
        super();
    }
    
    mounted() {
        
    }
    
    onStartClicked() {
        Socket.startGame();
    }

    onLeaveRoom() {
        Socket.leaveRoom();
    }

 
}

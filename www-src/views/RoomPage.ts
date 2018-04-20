import Vue from 'vue';
import Component from "vue-class-component";
import { Prop } from "vue-property-decorator";
import { Socket } from '../utils';
import { WelcomePlayerCard } from "../components";

@Component({
    name:'room-page',
    template: `
    <div class="ui one column center aligned grid container">
        <div class="column">
            <h1>Room {{roomId}} <button class="ui button" @click="onLeaveRoom">Leave</button></h1>
            <div class="ui relaxed grid">
                <div class="two column row">
                    <div class="column">
                        <welcome-player-card v-bind:playerName="viewModel.roomInfo ? viewModel.roomInfo.blackPlayerName : ''"
                         side="black" />
                    </div>
                    <div class="column">
                        <welcome-player-card v-bind:playerName="viewModel.roomInfo ? viewModel.roomInfo.whitePlayerName : ''"
                         side="white" />
                    </div>
                </div>
                <div class="one column row">
                    <div class="column middle aligned">
                        <button class="big ui button" @click="onStartClicked">Start Game</button>
                    </div>
                </div>
            </div>
        </div>
    </div>`,
    components: {WelcomePlayerCard}
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

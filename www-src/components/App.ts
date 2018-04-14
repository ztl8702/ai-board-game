import Vue from 'vue';
import { PlayBoard } from "./PlayBoard";
import { WelcomePage } from "./WelcomePage";
import { RoomPage } from "./RoomPage";
import { BoardPage } from "./BoardPage";
import { ClientViewModel } from '../models/ClientViewModel';
import { Socket } from '../utils';


export var App = Vue.extend({
    template: `
    <div>
        current page: {{vm.page}} your name: {{vm.playerName}} <button @click="onChangeName">Change</button>
        <welcome-page v-if="vm.page == 'welcome'" v-bind:playerName="vm.playerName" />
        <room-page v-bind:roomId="vm.roomId" v-bind:viewModel="vm" v-if="vm.page=='room'"/>
        <board-page v-bind:viewModel="vm" v-if="vm.page=='board'"/>
    </div>`,
    components: { PlayBoard, WelcomePage, RoomPage, BoardPage },
    data: () => {
        return {
            'vm': new ClientViewModel()
        };
    },
    mounted: () => {

    },

    methods: {
        onChangeName: () => {
            var name = window.prompt("What nickname do you want?");
            if (name && name.length > 0) {
                Socket.setNickname(name);
            }
        }

    }
});


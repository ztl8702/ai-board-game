import Vue from 'vue';
import { PlayBoard } from "./components";
import { BoardPage, RoomPage, WelcomePage } from "./views";
import { ClientViewModel } from './models/ClientViewModel';
import { Socket } from './utils';


export var App = Vue.extend({
    template: `
    <div>
        <div class="ui stackable menu">
            <a class="active item">
            current page: {{vm.page}}
            </a>
            <div class="right menu">
                <a class="ui item">
                Welcome, {{vm.playerName}} (<a @click="onChangeName">Change</a>)
                </a>
            </div>
        </div>
        
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


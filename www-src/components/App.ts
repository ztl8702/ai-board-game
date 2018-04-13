import Vue from 'vue';
import {PlayBoard} from "./PlayBoard";

new Vue({
    el: '#app',
    template: `
        <play-board />`,
    components: { PlayBoard }
  });

console.log('App loaded');
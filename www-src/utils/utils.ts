import * as faker from "faker";
function getRandomRoomId() {
    var str = faker.hacker.adjective() + '_' + faker.hacker.noun();
    str.replace(/ /g, '_');
    str.replace(/-/g, '_');
    return str;
}
## Conceptual Design

- All game logic happen on the server side
- Client side utilises some game logic for UI, but client side operations are not binding.
- When a user connects, the server code creates a `Player` object in memory to represent the user. This object will persist even if the user disconnects or their browser refreshes. The user is identified by cookie.
- When a user joins a room, if the room with given `roomId` did not exist, an `GameRoom` object will be created to represent that.
- `GameRoom` will have multiple `GameSession`s.

## Development

### Prerequisite

1. Ensure that you have the following installed:
 - node
 - yarn
 - npm

2. Clone this repository:

    ```
    git clone https://github.com/ztl8702/comp30024-ai-project
    cd comp30024-ai-project
    git checkout online-game
    ```

3. Run:
    ```
    yarn install
    yarn global add gulp-cli
    ```

### Run the development server

1. Execute:
    ```
    npm run run
    ```

1. Go to the browser and visit `http://localhost:3000`

1. Use a different browser (or incognito mode) to simulate multiple users
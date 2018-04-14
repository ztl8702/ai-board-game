FROM node:8 as build-env

WORKDIR /app


RUN yarn global add gulp-cli typescript

COPY . ./

RUN yarn install --production=false

RUN gulp frontend:rebuild && tsc 

FROM node:8-alpine
WORKDIR /app
COPY --from=build-env /app/package.json ./
COPY --from=build-env /app/yarn.lock ./
RUN yarn install
COPY --from=build-env /app/src ./src
COPY --from=build-env /app/public ./public
RUN ls -la
ENTRYPOINT [ "node", "src/index.js"]
import config from "./config";

export default function ws_light () { 
    const URL_WEB_LOGIN = `ws://${config.host}:${config.port}/light_ws/light_ws` 
    const websocket = new WebSocket(URL_WEB_LOGIN);
    return websocket;
}
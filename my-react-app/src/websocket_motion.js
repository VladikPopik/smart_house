import config from "./config";

export default function ws_motion () { 
    const URL_WEB_LOGIN = `ws://${config.host}:${config.port}/mon_ws/monitoring_ws` 
    const websocket = new WebSocket(URL_WEB_LOGIN);
    return websocket;
}
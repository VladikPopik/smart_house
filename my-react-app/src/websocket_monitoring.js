import config from "./config";

export default function ws_monitoring () { 
    const URL_WEB_LOGIN = `ws://${config.host}:${config.port}/mon_ws/monitoring_ws` 
    const websocket = new WebSocket(URL_WEB_LOGIN);
    return websocket;
}
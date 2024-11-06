import { Box, Grid, ImageList, Stack } from "@mui/material";
import { Alert } from "@mui/material";
import CheckIcon from '@mui/icons-material/Check';
import { useEffect, useState } from "react";
import config from "../config";
import Grid2 from "@mui/material/Unstable_Grid2";
import ErrorIcon from '@mui/icons-material/Error';
import WarningIcon from '@mui/icons-material/Warning';
import InfoIcon from '@mui/icons-material/Info';
import ImageListItem from '@mui/material/ImageListItem';

export default function AlertStack (message="motion") {
    var stack_len = 0;

    const URL_WEB_LOGIN = `ws://${config.host}:${config.port}/motion_ws/motion_ws` 
    const URL_WEB_SOCKET = `ws://${config.host}:${config.port}/motion_ws/motions_ws` 


    var [alerts, setAlerts] = useState(["no data", "no data", "no data", "no data"]);
    let newdt = (+new Date())/1000;
    const [timings, setTime] = useState([newdt, newdt, newdt, newdt]);

    const addItem = (event) => {
        const dt = JSON.parse(event.data);
        const status = dt.status;
        let newt = dt.time
        
        setAlerts(prevItems => [...prevItems, status]);
        setTime(prevItems => [...prevItems, newt])
    };

    useEffect(() => {
        const websocket = new WebSocket(URL_WEB_LOGIN);

        websocket.onmessage = function(event) {
            addItem(event)
            websocket.send("recieved")
        }

        websocket.onopen = () => {
            websocket.send(message);
        }
        return () => {
            websocket.close(1000, message+"over");
        }
    }, []);


    const hash = new Map();
    hash.set("success", <CheckIcon/>)
    hash.set("error", <ErrorIcon/>)
    hash.set("info", <InfoIcon/>)
    hash.set("warning", <WarningIcon/>)


    return (
        <Grid2 sx={{alignContent: "center", justifyContent: "center", display: "flex"}}>
            <ImageList sx={{width: "75%", height: "75%", justifyContent: "center", alignContent: "center", display: "flex"}}>
                <ImageListItem sx={{height: "75%", width: "75%", alignContent: "center", justifyContent: "center"}}>
                    <img
                        src={"./src/assets/3.jpg"}
                        alt={"Detected something"}
                        loading="eager"
                    />
                    </ImageListItem>
            </ImageList>
            <Stack sx={{
                display: "grid",
                alignContent: "center",
                justifyContent: "center",
                height: "75%",
                width: "75%", 
            }}>
                {
                    alerts.slice(alerts.length-5, -1).map(
                        (items, i) => (
                            <Alert icon={hash[items]} severity={items} sx={{width: "200px", height: "75px", display: "flex", alignContent: "center"}}>
                                {items} at  {new Date(timings[i]*1000).toISOString()}          
                            </Alert>
                        )
                    )
                }
            </Stack>
        </Grid2>
    )
}
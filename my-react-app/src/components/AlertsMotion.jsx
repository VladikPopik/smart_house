import { Box, Grid, ImageList, Stack } from "@mui/material";
import { Alert } from "@mui/material";
import CheckIcon from '@mui/icons-material/Check';
import { useEffect, useState, useRef } from "react";
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


    let newdt = (+new Date())/1000;

    const localalerts = localStorage.getItem("alerts");
    const localdt = localStorage.getItem("timings");

    const localAlerts = (localalerts !== null && localalerts !== 'null') ? 
        localalerts.split(','): [];

    const localTime = (localdt !== null && localdt !== 'null') ? 
        localdt.split(',').map(x => parseFloat(x)): [newdt];

    var [alerts, setAlerts] = useState(
        localAlerts
    );
    const [timings, setTime] = useState(localTime);
    const [pixelArray, setImage] = useState(new Uint8ClampedArray(480 * 600 * 4).fill(255));

    const addItem = (event) => {
        const dt = JSON.parse(event.data);
        const status = dt.status;
        let newt = dt.time
        let img = dt.image
        
        setAlerts(prevItems => [...prevItems, status]);
        setTime(prevItems => [...prevItems, newt]);
        setImage(dt.image.flat().flat());
        // localStorage.setItem("alerts", [alerts])
        // localStorage.setItem("timings", [timings])
    };

    const canvasRef = useRef(null);

    const [imageUrl, setImageUrl] = useState('');
  

    useEffect(() => {
        const websocket = new WebSocket(URL_WEB_LOGIN);

        websocket.onmessage = function(event) {
            addItem(event)
            websocket.send("recieved")
        }

        websocket.onopen = () => {
            websocket.send("motion");
        }
        return () => {
            websocket.close(1000, "motion" + "over");
        }
    }, []);


    const hash = new Map();
    hash.set("success", <CheckIcon/>)
    hash.set("error", <ErrorIcon/>)
    hash.set("info", <InfoIcon/>)
    hash.set("warning", <WarningIcon/>)

    localStorage.setItem("alerts", alerts)
    localStorage.setItem("timings", timings)
    //TODO: Fix alerts
    if (alerts.length <= 5)
    {
        var temp = alerts.reverse().map(
            (items, i) => (
                <Alert icon={hash[items]} severity={items} sx={{width: "200px", height: "75px", display: "flex", alignContent: "center"}}>
                    {items} at  {new Date(timings.reverse()[i]*1000).toISOString().split("T")[1].slice(0, -5)}          
                </Alert>
            )
        )
    }else{
        var temp = alerts.slice(-6, -1).reverse().map(
            (items, i) => (
                <Alert icon={hash[items]} severity={items} sx={{width: "200px", height: "75px", display: "flex", alignContent: "center"}}>
                    {items} at  {new Date(timings.reverse()[i]*1000).toISOString().split("T")[1].slice(0, -5)}          
                </Alert>
            )
        )
        var temp_t = timings.slice(-6, -1)
        var temp_a = alerts.slice(-6, -1);
    }

    // const canvas = document.getElementById('myCanvas');
    // const ctx = canvas.getContext('2d');
    // var imageDataObj = new ImageData(pixelArray, 480, 640);
    // ctx.putImageData(imageDataObj, 0, 0);
    // const imageUrl = canvas.toDataURL('image/png');
    // const img = new Image();
    // img.src = imageUrl;
    // document.body.appendChild(img);
    var url =  "./src/assets/test2e3ef4f2-0c44-4cea-b2cc-02b27693e92d.jpg";
    return (
        <Grid2 sx={{alignContent: "center", justifyContent: "center", display: "flex"}}>
            <ImageList sx={{width: "1000%", height: "1000%", justifyContent: "center", alignContent: "center"}}>
                <ImageListItem sx={{height: "100%", width: "100%", alignContent: "center", justifyContent: "center"}}>
                    <img
                        src={url}
                        alt={"Detected something"}
                        loading="eager"
                    />
                    </ImageListItem>
            </ImageList>
            {/* <img src={pixelsToCanvas(img, 480, 640).src}/> */}
            <Stack sx={{
                display: "grid",
                alignContent: "center",
                justifyContent: "center",
                height: "100%",
                width: "100%", 
            }}>
                {
                    temp
                }
            </Stack>
        </Grid2>
    )
}
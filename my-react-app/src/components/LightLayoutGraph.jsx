import React, { useState, useEffect, useRef } from "react";
import { useNavigate } from "react-router-dom";
import { LineChart } from '@mui/x-charts/LineChart';
import config from "../config";
import { Box, Button, Grid, Stack } from "@mui/material";
import { Gauge, gaugeClasses } from '@mui/x-charts/Gauge';
import { BarChart } from "@mui/x-charts";
import ws_light from "../websocket_light";
import AlertError from "./Alert";


export default function LightCharts (message="light") { 

    let newdt = (+new Date())/1000;

    var lux = localStorage.getItem("lux");
    var infrared = localStorage.getItem("infrared");
    var visible = localStorage.getItem("visible");
    var full_spectrum = localStorage.getItem("full_spectrum");
    var time = localStorage.getItem("light_time");

    lux = (lux !== null && lux !== 'null') ? 
        lux.split(',').map(x => parseFloat(x)): [0];

    infrared = (infrared !== null && infrared !== 'null') ? 
    infrared.split(',').map(x => parseFloat(x)): [0];
    
    visible = (visible !== null && visible !== 'null') ? 
    visible.split(',').map(x => parseFloat(x)): [0];

    full_spectrum = (full_spectrum !== null && full_spectrum !== 'null') ? 
    full_spectrum.split(',').map(x => parseFloat(x)): [0];
        
    time = (time !== null && time !== 'null') ? 
    time.split(',').map(x => parseFloat(x)): [newdt];

    var [ws_lux, setLux] = useState(lux);
    var [ws_infrared, setInfrared] = useState(infrared);
    var [ws_visible, setVisible] = useState(visible);
    var [ws_full_spectrum, setFull] = useState(full_spectrum);
    var [timings, setTime] = useState(time);
    var [error, setError] = useState("");
    var [error_code, setErrorCode] = useState(0);


    const handleClick = () => {
        localStorage.setItem("lux", result_lux.at(-1));
        localStorage.setItem("infrared", result_infrared.at(-1));
        localStorage.setItem("visible", result_visible.at(-1));
        localStorage.setItem("full_spectrum", result_full_spectrum.at(-1));
        localStorage.setItem("light_time", time_result.at(-1));
        window.location.reload();
    }

    const addItem = (event) => {
        const dt = JSON.parse(event.data);
        if (dt){
            const new_lux = dt.lux;
            const new_infrared = dt.infrared;
            const new_visible = dt.visible;
            const new_full_spectrum = dt.full_spectrum;
            let newt = dt.time;
            const error = dt.error;
            const error_code = dt.error_code;
            setLux(prevItems => [...prevItems, new_lux])
            setInfrared(prevItems => [...prevItems, new_infrared]);
            setVisible(prevItems => [...prevItems, new_visible])
            setFull(prevItems => [...prevItems, new_full_spectrum]);
            setTime(prevItems => [...prevItems, newt])
            setError(error);
            setErrorCode(error_code);
        }
    };

    useEffect(() => {
        const websocket = ws_light();

        websocket.onmessage = function(event) {
            addItem(event)
            websocket.send("recieved")
        }

        websocket.onopen = () => {
            websocket.send("light");
        }
        return () => {
            if (websocket.CLOSED){
                websocket.close(1000, "light"+" over");
            }
        }
    }, []);

    if (ws_lux.length > 60){
        var time_result = timings.slice(timings.length - 60, -1);
        var result_lux  = ws_lux.slice(ws_lux.length - 60, -1);
        var result_infrared = ws_infrared.slice(ws_infrared.length - 60, -1);
        var result_visible  = ws_visible.slice(ws_visible.length - 60, -1);
        var result_full_spectrum  = ws_full_spectrum.slice(ws_full_spectrum.length - 60, -1);

        setInfrared(prevItems => result_infrared)
        setLux(prevItems => result_lux);
        setVisible(prevItems => result_visible)
        setFull(prevItems => result_full_spectrum);
        setTime(prevItems => time_result)

    }else{
        var time_result = timings;
        var result_lux  = ws_lux;
        var result_infrared = ws_infrared;
        var result_visible  = ws_visible;
        var result_full_spectrum  = ws_full_spectrum;
    }
    localStorage.setItem("lux", result_lux);
    localStorage.setItem("infrared", result_infrared);
    localStorage.setItem("visible", result_visible);
    localStorage.setItem("full_spectrum", result_full_spectrum);
    localStorage.setItem("light_time", time_result);

    return (
            <Stack 
                direction="column"
                sx={{width: 1900, height: 920}}
            >
                <Grid
                sx={
                    {
                        height: "50%",
                        position: "absolute",
                        top: 100,
                        left: 50
                    }
                }>
                    <LineChart
                        xAxis={[{ 
                        data:  timings, scaleType: 'point', 
                        valueFormatter: (value) => {return new Date(value*1000).toISOString().split("T")[1].slice(0, -5)}}]}
                        skipAnimation
                        series={[
                            {
                                curve: "monotoneX",
                                data: result_lux,
                                type: 'line',
                                label: 'Свет, Люкс',
                                color: 'yellow',
                                baseline: 0,
                            },
                            
                        ]}
                        width={1300}
                        height={450}
                        grid={{vertical: true, horizontal: true}}
                    />
                    <LineChart
                        xAxis={[{ 
                        data:  timings, scaleType: 'point', 
                        valueFormatter: (value) => {return new Date(value*1000).toISOString().split("T")[1].slice(0, -5)}}]}
                        skipAnimation
                        series={[
                            {
                                curve: "monotoneX",
                                label: 'Видимый свет',
                                type: 'line',
                                data: result_visible,
                                color: 'yellow',
                                baseline: 0,
                            },
                            {
                                curve: "monotoneX",
                                data: result_full_spectrum,
                                type: 'line',
                                label: 'Полный спектр',
                                color: 'green',
                                baseline: 0,
                            },
                        ]}
                        width={1300}
                        height={450}
                        grid={{vertical: true, horizontal: true}}
                    />
                
                </Grid>
                <Button
                    sx={
                        {
                            height: "5%",
                            position: "absolute",
                            right: 500,
                            top: 750,
                            backgroundColor: "#228BE6",
                            color: "#ffffff",
                        }
                    }
                    variant="contained"
                    onClick={handleClick}
                >
                Обновить графики
                </Button>
                <AlertError
                    error={error}
                    error_code={error_code}
                />
            </Stack>
    )
}
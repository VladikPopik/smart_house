import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { LineChart } from '@mui/x-charts/LineChart';
import config from "../config";
import { Box, Grid, Stack } from "@mui/material";
import { Gauge, gaugeClasses } from '@mui/x-charts/Gauge';
import { BarChart } from "@mui/x-charts";

export default function MonitoringCharts (message="monitoring") { 

    let newdt = (+new Date())/1000;

    const localt = localStorage.getItem("temperature");
    const localh = localStorage.getItem("humidity");
    const localdt = localStorage.getItem("monitoring_time");

    const localTemperature = (localt !== null && localt !== 'null') ? 
        localt.split(',').map(x => parseFloat(x)): [0];

    const localHumidity = (localh !== null && localh !== 'null') ? 
        localh.split(',').map(x => parseFloat(x)): [0];
    
    const localTime = (localdt !== null && localdt !== 'null') ? 
        localdt.split(',').map(x => parseFloat(x)): [newdt];

    var [temperature, setTemperature] = useState(localTemperature);
    var [humidity, setHumidity] = useState(localHumidity);
    var [timings, setTime] = useState(localTime);
    const URL_WEB_LOGIN = `ws://${config.host}:${config.port}/mon_ws/monitoring_ws` 

    const addItem = (event) => {
        const dt = JSON.parse(event.data);
        if (dt){
            const newd = dt.temperature;
            const newh = dt.humidity;
            let newt = dt.time
            setHumidity(prevItems => [...prevItems, newh])
            setTemperature(prevItems => [...prevItems, newd]);
            setTime(prevItems => [...prevItems, newt])
        }
    };
    useEffect(() => {
        const websocket = new WebSocket(URL_WEB_LOGIN);

        websocket.onmessage = function(event) {
            addItem(event)
            websocket.send("recieved")
        }

        websocket.onopen = () => {
            websocket.send("monitoring");
        }
        return () => {
            if (websocket.CLOSED){
                websocket.close(1000, "monitoring"+" over");
            }
        }
    }, []);
    if (temperature.length > 60){
        var t_result = timings.slice(timings.length - 60, -1);
        var result  = temperature.slice(temperature.length - 60, -1);
        var result_h = humidity.slice(humidity.length - 60, -1)

        setHumidity(prevItems => result_h)
        setTemperature(prevItems => result);
        setTime(prevItems => t_result)

    }else{
        var t_result = timings;
        var result  = temperature;
        var result_h = humidity;
    }
    var latest_T = (temperature.at(-1))
    if (!latest_T){
        latest_T = 0
    }else{
        latest_T = latest_T.toFixed(1)
    }
    let gauge_coefficient = humidity.slice(-2, -1);
    if (gauge_coefficient){
        gauge_coefficient = Math.round(gauge_coefficient).toFixed(1);
    }else{
        gauge_coefficient = 0
    }

    localStorage.setItem("temperature", result);
    localStorage.setItem("humidity", result_h);
    localStorage.setItem("monitoring_time", t_result);

    return (
            <Stack 
                direction="column"
                sx={{width: 1800, height: 920}}
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
                        xAxis={[{ data:  timings, valueFormatter: (value) => {return new Date(value*1000).toISOString().split("T")[1].slice(0, -5)}}]}
                        series={[
                            {
                                curve: "monotoneX",
                                data: humidity,
                                area: true,
                                color: '#00ff00',
                                baseline: 0,
                        },
                        ]}
                        width={1300}
                        height={450}
                        grid={{vertical: true, horizontal: true}}
                    />
                    <LineChart
                        xAxis={
                            [
                                {
                                     data:  timings,
                                     valueFormatter: (value) => 
                                        {return new Date(value*1000).toISOString().split("T")[1].slice(0, -5)}
                                }
                            ]
                        }

                        series={[
                            {
                                curve: "monotoneX",
                                data: temperature,
                                area: true,
                                color: '#00ff00',
                                baseline: -50
                        },
                        ]}
                        width={1300}
                        height={450}
                        grid={{vertical: true, horizontal: true}}
                    />
                </Grid>

                <Grid 
                    sx={
                        {
                            width: "25%",
                            height: "25%",
                            position: "absolute",
                            right: 50,
                            top: 150
                        }
                    }
                >
                    <Gauge
                    value={gauge_coefficient}
                    startAngle={-90}
                    endAngle={90}
                    valueMax={100}
                    sx={{
                        [`& .${gaugeClasses.valueText}`]: {
                            width: "50%",
                            height: "50%"
                        },
                    }}
                    text={
                        ({ value, valueMax }) => value
                    }
                    />
                    <BarChart
                        xAxis={
                            [
                                {
                                    scaleType: 'band',
                                    data: ["T"]
                                }
                            ]
                        }
                        series={
                            [
                                {
                                    data: [latest_T]
                                }
                            ]
                        }
                        height={500}
                        borderRadius={13}
                        sx={{color:"blue",
                            height: "8%",
                            width: "10%"
                        }}
                    />
                </Grid>
            </Stack>
    )
}
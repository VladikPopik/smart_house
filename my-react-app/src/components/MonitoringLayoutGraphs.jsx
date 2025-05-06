import React, { useState, useEffect, useRef } from "react";
import { useNavigate } from "react-router-dom";
import { LineChart } from '@mui/x-charts/LineChart';
import config from "../config";
import { Box, Button, Grid, Stack } from "@mui/material";
import { Gauge, gaugeClasses } from '@mui/x-charts/Gauge';
import { BarChart } from "@mui/x-charts";
import ws_monitoring from "../websocket_monitoring";

export default function MonitoringCharts (message="monitoring") { 

    let newdt = (+new Date())/1000;

    const localt = localStorage.getItem("temperature");
    const localh = localStorage.getItem("humidity");
    const localt_max = localStorage.getItem("temperature_max");
    const localt_min = localStorage.getItem("temperature_min");
    const localh_max = localStorage.getItem("humidity_max");
    const localh_min = localStorage.getItem("humidity_min");
    const localdt = localStorage.getItem("monitoring_time");

    const localTemperature = (localt !== null && localt !== 'null') ? 
        localt.split(',').map(x => parseFloat(x)): [0];

    const localHumidity = (localh !== null && localh !== 'null') ? 
        localh.split(',').map(x => parseFloat(x)): [0];
    
    const localTemperature_max = (localt_max !== null && localt_max !== 'null') ? 
        localt_max.split(',').map(x => parseFloat(x)): [0];

    const localHumidity_max = (localh_max !== null && localh_max !== 'null') ? 
        localh_max.split(',').map(x => parseFloat(x)): [0];
        
    const localTemperature_min = (localt_min !== null && localt_min !== 'null') ? 
        localt_min.split(',').map(x => parseFloat(x)): [0];

    const localHumidity_min = (localh_min !== null && localh_min !== 'null') ? 
        localh_min.split(',').map(x => parseFloat(x)): [0];
    
    const localTime = (localdt !== null && localdt !== 'null') ? 
        localdt.split(',').map(x => parseFloat(x)): [newdt];

    var [temperature, setTemperature] = useState(localTemperature);
    var [humidity, setHumidity] = useState(localHumidity);
    var [temperature_max, setTemperatureMax] = useState(localTemperature_max);
    var [humidity_max, setHumidityMax] = useState(localHumidity_max);
    var [temperature_min, setTemperatureMin] = useState(localTemperature_min);
    var [humidity_min, setHumidityMin] = useState(localHumidity_min);
    var [timings, setTime] = useState(localTime);

    const handleClick = () => {
        localStorage.setItem("temperature", result.at(-1));
        localStorage.setItem("humidity", result_h.at(-1));
        localStorage.setItem("temperature_max", result_t_max.at(-1));
        localStorage.setItem("temperature_min", result_t_min.at(-1));
        localStorage.setItem("humidity_max", result_h_max.at(-1));
        localStorage.setItem("humidity_min", result_h_min.at(-1));
        localStorage.setItem("monitoring_time", t_result.at(-1));
        window.location.reload();
    }

    const addItem = (event) => {
        const dt = JSON.parse(event.data);
        if (dt){
            const newd = dt.temperature;
            const newh = dt.humidity;
            const newd_max = dt.pred_temperature_max;
            const newd_min = dt.pred_temperature_min;
            const newh_max = dt.pred_humidity_max;
            const newh_min = dt.pred_humidity_min;
            let newt = dt.time;
            setHumidity(prevItems => [...prevItems, newh])
            setTemperatureMax(prevItems => [...prevItems, newd_max]);
            setHumidityMax(prevItems => [...prevItems, newh_max])
            setTemperatureMin(prevItems => [...prevItems, newd_min]);
            setHumidityMin(prevItems => [...prevItems, newh_min])
            setTemperature(prevItems => [...prevItems, newd]);
            setTime(prevItems => [...prevItems, newt])
        }
    };

    useEffect(() => {
        const websocket = ws_monitoring();

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
        var result_h = humidity.slice(humidity.length - 60, -1);
        var result_t_max  = temperature_max.slice(temperature_max.length - 60, -1);
        var result_t_min  = temperature_min.slice(temperature_min.length - 60, -1);
        var result_h_max  = humidity_max.slice(humidity_max.length - 60, -1);
        var result_h_min  = humidity_min.slice(humidity_min.length - 60, -1);

        setHumidity(prevItems => result_h)
        setTemperature(prevItems => result);
        setHumidityMax(prevItems => result_h_max)
        setHumidityMin(prevItems => result_h_min);
        setTemperatureMax(prevItems => result_t_max)
        setTemperatureMin(prevItems => result_t_min);
        setTime(prevItems => t_result)

    }else{
        var t_result = timings;
        var result  = temperature;
        var result_h = humidity;
        var result_t_max  = temperature_max;
        var result_t_min  = temperature_min;
        var result_h_max  = humidity_max;
        var result_h_min  = humidity_min;
    }
    var latest_T = (temperature.at(-1))
    if (!latest_T){
        latest_T = 0
    }else{
        latest_T = latest_T.toFixed(1)
    }
    let gauge_coefficient = humidity.at(-1);
    if (gauge_coefficient){
        gauge_coefficient = Math.round(gauge_coefficient).toFixed(1);
    }else{
        gauge_coefficient = 0
    }

    localStorage.setItem("temperature", result);
    localStorage.setItem("humidity", result_h);
    localStorage.setItem("temperature_max", result_t_max);
    localStorage.setItem("temperature_min", result_t_min);
    localStorage.setItem("humidity_max", result_h_max);
    localStorage.setItem("humidity_min", result_h_min);
    localStorage.setItem("monitoring_time", t_result);

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
                                data: result_h,
                                color: '#228BE6',
                                label: 'Влажность фактическая, %',
                                type: 'line',
                                baseline: 0,
                            },
                            {
                                curve: "monotoneX",
                                data: result_h_max,
                                type: 'line',
                                label: 'Влажность предсказанная верхняя граница, %',
                                color: '#ff0000',
                                baseline: 0,
                            },
                            {
                                curve: "monotoneX",
                                label: 'Влажность предсказанная нижняя граница, %',
                                type: 'line',
                                data: result_h_min,
                                color: '#ff0000',
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
                                     scaleType: 'point',
                                     valueFormatter: (value) => 
                                        {return new Date(value*1000).toISOString().split("T")[1].slice(0, -5)}
                                }
                            ]
                        }
                        skipAnimation
                        series={[
                            {
                                curve: "monotoneX",
                                type: 'line',
                                data: result,
                                label: 'Температура фактическая, С',
                                color: '#228BE6',
                                baseline: -50
                            },
                            {
                                curve: "monotoneX",
                                type: 'line',
                                label: 'Температура предсказанная верхняя граница, С',
                                data: result_t_max,
                                color: '#ff0000',
                            },
                            {
                                curve: "monotoneX",
                                type: 'line',
                                label: 'Температура предсказанная нижняя граница, С',
                                data: result_t_min,
                                color: '#ff0000',
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
                            width: "100%",
                            height: "100%"
                        },[`& .${gaugeClasses.valueArc}`]: {
                            fill: '#228BE6',
                          },
                    }}
                    text={
                        ({ value, valueMax }) => `${value}`
                    }
                    />
                    <BarChart
                    colors={["#228BE6"]}
                        xAxis={
                            [
                                {
                                    scaleType: 'band',
                                    data: ["T"],
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
                    />
                <Button
                    sx={
                        {
                            height: "25%",
                            position: "absolute",
                            right: 50,
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
                </Grid>
            </Stack>
    )
}
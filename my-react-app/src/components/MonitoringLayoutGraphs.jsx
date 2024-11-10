import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { LineChart } from '@mui/x-charts/LineChart';
import config from "../config";
import { Box, Grid } from "@mui/material";
import { Gauge, gaugeClasses } from '@mui/x-charts/Gauge';
import { BarChart } from "@mui/x-charts";

export default function MonitoringCharts (message="monitoring") { 
    const [data, setData] = useState([0]);
    let newdt = (+new Date())/1000;
    const [timings, setTime] = useState([newdt]);
    const URL_WEB_LOGIN = `ws://${config.host}:${config.port}/mon_ws/monitoring_ws` 


    const addItem = (event) => {
        const dt = JSON.parse(event.data);
        const newd = dt.value;
        
        let newt = dt.time
        
        setData(prevItems => [...prevItems, newd]);
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
            if (websocket.CLOSED){
                websocket.close(1000, message+"over");
            }
        }
    }, []);
    if (data.length > 30){
        var t_result = timings.slice(timings.length - 30, -1);
        var result  = data.slice(data.length - 30, -1);
    }else{
        var t_result = timings;
        var result  = data;
    }
    const latest_T = (data.at(-1) * 100).toFixed(1)
    let gauge_coefficient = result.slice(-2, -1);

    gauge_coefficient = Math.round(gauge_coefficient*100)/100;
    
    return (
        <div style={{position: "absolute", left: 50, top: 100, width: "95%"}}>
            <Box>
                <Grid sx={{position: "absolute", alignContent: "left", justifyContent: "center", alignSelf: "start"}}>
                    <LineChart
                        skipAnimation
                        xAxis={[{ data:  t_result, valueFormatter: (value) => {return new Date(value*1000).toISOString().split("T")[1].slice(0, -5)}}]}
                        series={[
                            {
                                curve: "monotoneX",
                                data: result,
                                area: true,
                                color: '#00ff00'
                        },
                        ]}
                        width={700}
                        height={400}
                        grid={{vertical: true, horizontal: true}}
                    />
                    <LineChart
                        skipAnimation
                        xAxis={[{ data:  t_result, valueFormatter: (value) => {return new Date(value*1000).toISOString().split("T")[1].slice(0, -5)}}]}
                        series={[
                            {
                                curve: "monotoneX",
                                data: result,
                                area: true,
                                color: '#00ff00'
                        },
                        ]}
                        width={700}
                        height={400}
                        grid={{vertical: true, horizontal: true}}
                    />
                </Grid>
                <Grid sx={{position: "absolute", alignContent: "left", justifyContent: "center", alignSelf: "right", right: 350}}>
                    <LineChart
                        skipAnimation
                        xAxis={[{ data:  t_result, valueFormatter: (value) => {return new Date(value*1000).toISOString().split("T")[1].slice(0, -5)}}]}

                        series={[
                            {
                                curve: "monotoneX",
                                data: result,
                                area: true,
                                color: '#00ff00'
                        },
                        ]}
                        width={700}
                        height={400}
                        grid={{vertical: true, horizontal: true}}
                    />
                    <LineChart
                        skipAnimation
                        xAxis={[{ data:  t_result, valueFormatter: (value) => {return new Date(value*1000).toISOString().split("T")[1].slice(0, -5)}}]}

                        series={[
                            {
                                curve: "monotoneX",
                                data: result,
                                area: true,
                                color: '#00ff00'
                        },
                        ]}
                        width={700}
                        height={400}
                        grid={{vertical: true, horizontal: true}}
                    />
                </Grid>
                <Grid sx={{position: "absolute", alignContent: "right", justifyContent: "end", alignSelf: "right", right: 0, width: 250, height: 500}}>
                    <Gauge
                    value={gauge_coefficient}
                    startAngle={-120}
                    endAngle={120}
                    valueMax={1}
                    sx={{
                        [`& .${gaugeClasses.valueText}`]: {
                        fontSize: 40,
                        transform: 'translate(0px, 0px)',
                        },
                    }}
                    text={
                        ({ value, valueMax }) => `${value} / ${valueMax}`
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
                        height={300}
                        borderRadius={13}
                        barLabel="value"
                        sx={{color:"blue"}}
                    />
                </Grid>
            </Box>
    </div>
    )
}
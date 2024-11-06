import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { LineChart } from '@mui/x-charts/LineChart';
import config from "../config";
import { Box, Grid } from "@mui/material";
import { Gauge, gaugeClasses } from '@mui/x-charts/Gauge';
import { BarChart } from "@mui/x-charts";

export default function MonitoringCharts () { 
    const [data, setData] = useState([0]);
    let newdt = (+new Date())/1000;
    const [timings, setTime] = useState([newdt]);
    const URL_WEB_LOGIN = `ws://${config.host}:${config.port}/mon_ws/monitoring_ws` 
    const URL_WEB_SOCKET = `ws://${config.host}:${config.port}/mon_ws/monitoring_ws` 

    // const dateFormatter = 

    const addItem = (event) => {
        const dt = JSON.parse(event.data);
        const newd = dt.value;
        

        let newt = dt.time

        // newt = new Date(newt*1000);
        // console.log(newt, dt.time) 
        
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
            websocket.close();
        }
    }, []);
    const t_result = timings.slice(timings.length - 30, -1)
    const result  = data.slice(data.length - 30, -1);
    let gauge_coefficient = result.slice(-2, -1);

    gauge_coefficient = Math.round(gauge_coefficient*100)/100;
    
    return (
        <div style={{position: "absolute", left: 50, top: 100, width: "95%"}}>
            <Box>
                <Grid sx={{position: "absolute", alignContent: "left", justifyContent: "center", alignSelf: "start"}}>
                    <LineChart
                        skipAnimation
                        xAxis={[{ data:  t_result, valueFormatter: (value) => {return new Date(value*1000).toISOString()}}]}
                        series={[
                            {
                                curve: "monotoneX",
                                data: result,
                                area: true,
                                color: '#76db91'
                        },
                        ]}
                        width={700}
                        height={400}
                        // margin={{left: 100, top: 100}}
                        grid={{vertical: true, horizontal: true}}
                        
                        // sx={{}}
                        // position: "absolute", left: 0, top: 0
                    />
                    <LineChart
                        skipAnimation
                        xAxis={[{ data:  t_result, valueFormatter: (value) => {return new Date(value*1000).toISOString()}}]}
                        series={[
                            {
                                curve: "monotoneX",
                                data: result,
                                area: true,
                                color: '#76db91'
                        },
                        ]}
                        width={700}
                        height={400}
                        // margin={{left: 100, top: 100}}
                        grid={{vertical: true, horizontal: true}}
                        // sx={{}}
                        // position: "absolute", left: 0, top: 0
                    />
                </Grid>
                <Grid sx={{position: "absolute", alignContent: "left", justifyContent: "center", alignSelf: "right", right: 350}}>
                    <LineChart
                        skipAnimation
                        xAxis={[{ data:  t_result, valueFormatter: (value) => {return new Date(value*1000).toISOString()}}]}

                        series={[
                            {
                                curve: "monotoneX",
                                data: result,
                                area: true,
                                color: '#76db91'
                        },
                        ]}
                        width={700}
                        height={400}
                        // margin={{left: 100, top: 100}}
                        grid={{vertical: true, horizontal: true}}
                        // sx={{}}
                        // position: "absolute", left: 0, top: 0
                    />
                    <LineChart
                        skipAnimation
                        xAxis={[{ data:  t_result, valueFormatter: (value) => {return new Date(value*1000).toISOString()}}]}

                        series={[
                            {
                                curve: "monotoneX",
                                data: result,
                                area: true,
                                color: '#76db91'
                        },
                        ]}
                        width={700}
                        height={400}
                        // margin={{left: 100, top: 100}}
                        grid={{vertical: true, horizontal: true}}
                        // sx={{}}
                        // position: "absolute", left: 0, top: 0
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
                                    data: result
                                }
                            ]
                        }
                        height={300}
                        borderRadius={13}
                    />
                </Grid>
            </Box>
    </div>
    )
}
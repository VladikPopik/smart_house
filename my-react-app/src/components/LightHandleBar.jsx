import Button from '@mui/material/Button';
import Box from '@mui/material/Box';
import EmojiObjectsIcon from '@mui/icons-material/EmojiObjects';
import { useState } from 'react';
// import { color } from '@mui/system';
import Slider from '@mui/material/Slider';

export default function LightHandleBar() {
    const [error, setError] = useState('');
    const [time, setLightTime] = useState(5);


    const handleSliderChange = (event, value) => {
        setLightTime(value);
      };


    const handleColor = async (color) => {
        try {
            const response = await fetch('${config.protocol}://127.0.0.1:8000/lamp/' + color, {
            method: 'POST', 
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: JSON.stringify({
                'color': color, 
                'time': time 
            }), 
            }) 
            
            // if (response.ok){
            //     // setError("An error occured while trying to use diodes")
            // }

        } catch(error){
            setError('An error occured while trying to use diodes')
        }

        // const timer = setTimeout(() => console.log('Initial timeout!'), time);
        // clearTimeout(timer);

    }


    return (
        <div className='Big_div'>
            <Box
        sx={{
            alignItems: 'center',
            width: "100%", height: "125%",
            justifyContent: "center", 
            flexDirection: "row",
            display: "flex"
        }}
        >

        {/* <ButtonGroup variant="outlined" aria-label="Basic button group" sx={{height: "100%", width: "100%"}}> */}
            <Button 
            sx={
                {color: "white",
                backgroundColor: "red",
                width: "100%", 
                height: "100%", 
                margin: "25px"
                }
            }
            onClick={() => handleColor("RED")}
            >
                    

                <EmojiObjectsIcon />
            </Button>
            <Button sx={
                {color: "white",
                backgroundColor: "yellow",
                width: "100%", 
                height: "100%", 
                margin: "25px"
                }
            }
            onClick={() => handleColor("YELLOW")}
            >
                <EmojiObjectsIcon />
                
            </Button>
            <Button sx={
                {color: "white",
                backgroundColor: "green",
                width: "100%", 
                height: "100%", 
                margin: "25px"
                }
            }
            onClick={() => handleColor("GREEN")}
            >
                <EmojiObjectsIcon />
            </Button>
        {/* </ButtonGroup> */}
        </Box>
        <Slider
                size="small"
                defaultValue={5}
                min={5}
                max={60}
                aria-label="Small"
                valueLabelDisplay="auto"
                step={5}
                marks
                onChangeCommitted={handleSliderChange}  
            />
    </div>
    );
}
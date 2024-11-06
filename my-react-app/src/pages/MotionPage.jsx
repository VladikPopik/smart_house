import Motion from "../components/Motion";
import AppBarComponent from '../components/AppBarComponent.jsx';
import Button from "@mui/material/Button";

import { useNavigate } from "react-router-dom";
import { useState } from "react";
import SendIcon from '@mui/icons-material/Send';
import { IconButton } from "@mui/material";
import AlertStack from "../components/AlertsMotion.jsx";



export default function MotionPage() {
    const [error, setError] = useState('');
    const [loading, setLoading] = useState(false);
    const handleImitate = async (event) => {

        const formDetails = new URLSearchParams();


        try{
            const response = await fetch(`${config.protocol}://127.0.0.1:8081/insert`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                },
                body: formDetails
            });
        } catch (error) {
            setLoading(false);
            setError('An error occurred. Please try again later.');
        };
    }

    return (
        <div>
            <AppBarComponent />
            <Motion />
            <IconButton variant="contained" sx={{zIndex: 999999, position: 'absolute', top: 10, right: "95%", height: "300", color: "white"}} onClick={() => handleImitate()}>
                <SendIcon/>
            </IconButton>
            <AlertStack></AlertStack>
        </div>
    );
}
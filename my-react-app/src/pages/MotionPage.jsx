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
    return (
        <div>
            <AppBarComponent />
            <Motion />
            <AlertStack></AlertStack>
        </div>
    );
}
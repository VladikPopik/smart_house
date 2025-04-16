import { useNavigate } from "react-router-dom";
import AppBar from '@mui/material/AppBar';
import Box from '@mui/material/Box';
import IconButton from '@mui/material/IconButton';
import Toolbar from '@mui/material/Toolbar';
import LogoutIcon from '@mui/icons-material/Logout';
import HomeIcon from '@mui/icons-material/Home';
import { Button } from '@mui/material';
import DrawerComponent from "./DrawerComponent";

export default function AppBarComponent(){
    return(
        <div>
            <Box sx={{flexGrow: 1, top: 0, left:0, position: 'fixed', width: "100%", height: "100%", justifyContent: "centre"}}>
                
                <AppBar position='static' sx={{width: "100%", height: "10%", backgroundColor: "#228BE6"}}>
                    <Toolbar sx={{width: "100%", height: "100%", justifyContent: "centre"}}>
                    <h1 style={{position: 'absolute', top: "50%", left: '50%', transform: 'translate(-50%, -50%)'}}>&#127968; Мой Умный Дом &#127968;</h1>
                        <DrawerComponent />
                    </Toolbar>
                </AppBar>
            </Box>
        </div>
    )
} 
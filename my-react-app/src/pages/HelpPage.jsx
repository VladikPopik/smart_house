import { Card, CardMedia, Typography } from "@mui/material"
import AppBarComponent from "../components/AppBarComponent"
import Help from "../components/Help"
import CardContent from "@mui/material/CardContent"

export default function HelpPage (){
    return (
        <div>
            <AppBarComponent />
            <Help/>
            <Card sx={{position: "fixed", top: "12%", right: "30%", }}>
                <CardMedia
                    component="img"
                    height="50%"
                    width="50%"
                    image="src\assets\telegram_help.png"
                    alt="U+1F60E Scan QR code to join help Telegram chat"
                />
                <CardContent>
                    <Typography variant="h4"> 
                        <p>
                            &#128640; &#128640; &#128640; 
                            Scan QR code to join telegram chat for help
                            &#128640; &#128640; &#128640; 
                        </p> 
                    </Typography>
                </CardContent>
            </Card>
        </div>
    )
}
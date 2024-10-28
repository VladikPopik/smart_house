import AppBarComponent from "../components/AppBarComponent"
import Card from "@mui/material/Card"
import CardMedia from "@mui/material/CardMedia"
import Typography from "@mui/material/Typography"
import CardContent from "@mui/material/CardContent"

export default function TelegramPage (){
    return (
        <div>
            <AppBarComponent />
            <Card sx={{position: "fixed", top: "12%", right: "37.5%", width: "25%", height: "75%"}}>
                <CardMedia
                    component="img"
                    height="90%"
                    image="src\assets\telegram_motion.JPG"
                    alt="U+1F60E Scan QR code to join help Telegram chat"
                />
                <CardContent sx={{justifyContent: "center"}}>
                    <Typography variant="h6"> 
                        <p>
                            &#128640;  
                            Scan QR code to use telegram not for system alerts
                            &#128640;  
                        </p> 
                    </Typography>
                    <Typography variant="body" color="text.secondary" sx={{justifyContent: "center"}}>
                            Page for determining your economics for one month
                    </Typography>
                </CardContent>
            </Card>
        </div>
    )
}
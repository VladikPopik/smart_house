import Grid from "@mui/material/Grid";
import Card from "@mui/material/Card";
import CardActionArea from "@mui/material/CardActionArea";
import CardContent from "@mui/material/CardContent";
import CardMedia from "@mui/material/CardMedia";
import Typography from "@mui/material/Typography";
import { useNavigate } from "react-router-dom";

export default function CardHome() {
    const navigate = useNavigate();

    const handleMonitoring = () => {
        navigate('/monitoring');
    }

    const handleMotion = () => {
        navigate('/motion');
    }

    const handleLight = () => {
        navigate('/light');
    }

    return (
        <div>
            <Grid container spacing={2} sx={{ position: "absolute", top: "25%", justifyContent: "center"}}>
                <Card sx={{width: "40%", marginLeft: 5, backgroundColor: "aliceblue", marginRight: 20}}>
                    <CardActionArea
                        onClick={() => handleMonitoring()}
                    >
                        <CardMedia
                        component="img"
                        height="400"
                        image="src\assets\monitoring_prod.jpg"
                        alt="green iguana"
                        />
                        <CardContent>
                        <Typography gutterBottom variant="h5" component="div">
                            Мониторинг
                        </Typography>
                        <Typography variant="body2" color="text.secondary">
                            Модуль мониторинга Влажости и Температуры
                        </Typography>
                        </CardContent>
                    </CardActionArea>
                </Card>

                {/* <Card sx={{ width: "25%", marginRight:5, backgroundColor: "aliceblue"}}>
                    <CardActionArea
                        onClick={() => handleMotion()}
                    >
                        <CardMedia
                        component="img"
                        height="400"
                        image="src\assets\motion.jpg"
                        alt="green iguana"
                        />
                        <CardContent>
                        <Typography gutterBottom variant="h5" component="div">
                            Motion
                        </Typography>
                        <Typography variant="body2" color="text.secondary">
                            Page for motion functionallity
                        </Typography>
                        </CardContent>
                    </CardActionArea>
                </Card> */}

                <Card sx={{ width: "40%", marginLeft: 10, backgroundColor: "aliceblue"}}>
                    <CardActionArea
                        onClick={() => handleLight()}
                    >
                        <CardMedia
                        component="img"
                        height="400"
                        image="src\assets\3.jpg"
                        alt="green iguana"
                        />
                        <CardContent>
                        <Typography gutterBottom variant="h5" component="div">
                            Свет
                        </Typography>
                        <Typography variant="body2" color="text.secondary">
                            Модуль контроля света
                        </Typography>
                        </CardContent>
                    </CardActionArea>
                </Card>
            </Grid>
        </div>
    );
}
import AppBarComponent from "../components/AppBarComponent";
import MyFunctions from "../components/MyFunctions";
import Card from "@mui/material/Card";
import CardActionArea from "@mui/material/CardActionArea";
import CardContent from "@mui/material/CardContent";
import CardMedia from "@mui/material/CardMedia";
import Typography from "@mui/material/Typography";
import Grid from "@mui/material/Grid";
import { useNavigate } from "react-router-dom";

export default function MyFunctionsPage() {

    const navigate = useNavigate("");

    const handleCalendar = () => {
        navigate("/calendarplan")
    };

    // const handle

    return (
        <body>
            <AppBarComponent />
            <Grid container spacing={2} sx={{ position: "absolute", top: "25%", justifyContent: "center"}}>

                <Card sx={{width: "25%", marginLeft: 10}}>
                    <CardActionArea
                        onClick={() => handleCalendar()}
                    >
                        <CardMedia
                        component="img"
                        height="200"
                        image="src\assets\image.png"
                        alt="green iguana"
                        />
                        <CardContent>
                        <Typography gutterBottom variant="h5" component="div">
                            Monthly Plan
                        </Typography>
                        <Typography variant="body2" color="text.secondary">
                            Page for determining your economics for one month
                        </Typography>
                        </CardContent>
                    </CardActionArea>
                </Card>

                <Card sx={{ width: "25%", marginLeft: 10}}>
                    <CardActionArea>
                        <CardMedia
                        component="img"
                        height="140"
                        image="src\assets\image.png"
                        alt="green iguana"
                        />
                        <CardContent>
                        <Typography gutterBottom variant="h5" component="div">
                            Monthly Plan
                        </Typography>
                        <Typography variant="body2" color="text.secondary">
                            Page for determining your economics for one month
                        </Typography>
                        </CardContent>
                    </CardActionArea>
                </Card>

                <Card sx={{ width: "25%", marginLeft: 10}}>
                    <CardActionArea>
                        <CardMedia
                        component="img"
                        height="140"
                        image="\assets\telegram_help.svg"
                        alt="green iguana"
                        />
                        <CardContent>
                        <Typography gutterBottom variant="h5" component="div">
                            Monthly Plan
                        </Typography>
                        <Typography variant="body2" color="text.secondary">
                            Page for determining your economics for one month
                        </Typography>
                        </CardContent>
                    </CardActionArea>
                </Card>
            </Grid>
            <MyFunctions />
        </body>
    );
}
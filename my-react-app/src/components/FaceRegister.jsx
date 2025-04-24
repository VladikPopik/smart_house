import { useState } from "react";
import config from "../config";
import { Button, TextField } from "@mui/material";


export default function FaceRegister () { 

    const [error, setError] = useState('');
    const [login, setLogin] = useState('');
    const [, setLoading] = useState(false);

    const handleSubmit = async (event) => {
        event.preventDefault();
        setLoading(true);
        const user_login = localStorage.getItem("login");
        const formDetails = new URLSearchParams();
        formDetails.append("username", JSON.stringify(user_login));

        try {
            const response = await fetch(`${config.protocol}://${config.host}:${config.port}/auth/face/register`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/x-www-form-urlencoded",
                },
                body: JSON.stringify({user_login: user_login}),
            });
            setLoading(false);

            if (response.ok) {
                // if (response_token.ok){
                //     const data = await response_token.json();
                //     localStorage.setItem("token", data.access_token);
                // }
                const data = await response.json()
                if (data.success){
                    setLogin(data.login.user_login)
                }
            } else {
                const errorData = await response.json();
                setError(errorData.detail || "Ошибка регистрации!");
            }
        } catch (error) {
            console.log(error)
            setLoading(false);
            setError("Ошибка регистрации!");
        }
    };
    
    return (
        <div style={{"position": "absolute", "top": 125, "right": 350, "width": "25%", "height": "10%"}}>
            <br></br>
            <Button
                onClick={handleSubmit}
                variant="contained"
                sx={{width: "70%", height: "50%", backgroundColor: "#228BE6"}}
            >
                Регистрация с помощью фотографии
            </Button>
            {login && <p className="login" style={{ color: "green", width: "100%"}}>Пользователь успешно зарегистрирован {login}</p>}
            {error && <p className="error" style={{ color: "red" }}>{error}</p>}
        </div>
    )
    
}
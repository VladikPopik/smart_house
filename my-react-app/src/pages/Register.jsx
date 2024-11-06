import { useState } from "react";
import { useNavigate } from "react-router-dom";
import config from "../config";

function Register() {
    const [user_login, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [confirmPassword, setConfirmPassword] = useState('');
    const [email, setEmail] = useState('');
    const [tg_login, setTgLogin] = useState('');
    const [error, setError] = useState('');
    const [, setLoading] = useState(false);

    const navigate = useNavigate();

    const validateForm = () => {
        if (!user_login || !password || !confirmPassword || !email || !tg_login) {
            setError("All fields are required");
            return false;
        }

        if (password !== confirmPassword) {
                setError("Passwords do not match");
                return false;
        }
        if (!validateEmail(email)) {
            setError("Invalid email address");
            return false;
        }

        if (!validateTgLogin(tg_login)) {
            setError("Invalid Telegram login");
            return false;
        }

        setError("");
        return true;
    };

    const validateEmail = (email) => {
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return emailRegex.test(email);
    };

    const validateTgLogin = (tg_login) => {
        const tgLoginRegex = /^[a-zA-Z0-9_]+$/;
        return tgLoginRegex.test(tg_login);
    };


    const handleSubmit = async (event) => {
        event.preventDefault();
        if (!validateForm()) return;
        setLoading(true);

        const formDetails = new URLSearchParams();
        formDetails.append("username", JSON.stringify(user_login));
        formDetails.append("password",  JSON.stringify(password));
        formDetails.append("confirm_password", JSON.stringify(confirmPassword));
        formDetails.append("user_email", JSON.stringify(email));
        formDetails.append("tg_login", JSON.stringify(tg_login));
        formDetails.append("is_superuser", false);

        try {
            const response = await fetch(`${config.protocol}://${config.host}:${config.port}/auth/register`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/x-www-form-urlencoded",
                },
                body: JSON.stringify({user_login: user_login, password: password, confirm_password: confirmPassword, user_email: email, tg_login: tg_login, is_superuser: false}),
            });
            const username = user_login;
            const newFormDetails = new URLSearchParams();
            newFormDetails.append("username", username);
            newFormDetails.append("password", password);
            const response_token = await fetch(`${config.protocol}://${config.host}:${config.port}/auth/token`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/x-www-form-urlencoded",
                },
                body: newFormDetails,
            });            

            setLoading(false);

            if (response.ok) {
                if (response_token.ok){
                    const data = await response_token.json();
                    localStorage.setItem("token", data.access_token);
                }
                navigate("/home");
            } else {
                const errorData = await response.json();
                setError(errorData.detail || "Registration failed!");
            }
        } catch (error) {
            console.log(error)
            setLoading(false);
            setError("Registration failed!");
        }
    };

    return (
        <div className="login-form">
        <form onSubmit={handleSubmit} className="login">

            <div className="input-group">
                <input
                    type="text"
                    value={user_login}
                    onChange={(event) => setUsername(event.target.value)}
                    placeholder="Username"
                />
            </div>
            <div className="input-group">
                <input
                    type="password"
                    value={password}
                    onChange={(event) => setPassword(event.target.value)}
                    placeholder="Password"
                />
            </div>
                <div className="input-group">
                <input
                    type="password"
                    value={confirmPassword}
                    onChange={(event) => setConfirmPassword(event.target.value)}
                    placeholder="Confirm password"
                />
            </div>
                <div className="input-group">
            
                <input
                    type="email"
                    value={email}
                    onChange={(event) => setEmail(event.target.value)}
                    placeholder="Email"
                />
            </div>
                <div className="input-group">
                <input
                    type="text"
                    value={tg_login}
                    onChange={(event) => setTgLogin(event.target.value)}
                    placeholder="Telegram Login"
                />
            </div>

            {error && <p className="error" style={{ color: "red" }}>{error}</p>}
            <button type="submit">Register</button>
        </form>
        <a className="signup-link" href='/login'>Sign In</a>

        </div>
    );
}

export default Register;
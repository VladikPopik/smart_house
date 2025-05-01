import  { useState } from 'react';
import { useNavigate } from "react-router-dom";
import '../login.css';
import config from '../config';

function Login() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const navigate = useNavigate();

  const handlerClick = async (event) => {
    setLoading(true);
    try {
      const response = await fetch(`${config.protocol}://${config.host}:${config.port}/auth/token/face_recognition`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: {},
      });

      setLoading(false);

      if (response.ok) {
        const data = await response.json();
        localStorage.setItem('token', data.access_token);
        localStorage.setItem('login', username);
        navigate('/home');
      } else {
        const errorData = await response.json();
        setError(errorData.detail || 'Ошибка Ауентитификации');
      }
    } catch (error) {
      setLoading(false);
      setError('Ошибка. Пожалуйста, попробуйте позже');
    }
  }

  const validateForm = () => {
    if (!username || !password) {
      setError('Логин и пароль обязательны');
      return false;
    }
    setError('');
    return true;
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    if (!validateForm()) return;
    setLoading(true);

    const formDetails = new URLSearchParams();
    formDetails.append('username', username);
    formDetails.append('password', password);

    try {
      const response = await fetch(`${config.protocol}://${config.host}:${config.port}/auth/token`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: formDetails,
      });

      setLoading(false);

      if (response.ok) {
        const data = await response.json();
        localStorage.setItem('token', data.access_token);
        localStorage.setItem('login', username);
        navigate('/home');
      } else {
        const errorData = await response.json();
        setError(errorData.detail || 'Ошибка Ауентитификации');
      }
    } catch (error) {
      setLoading(false);
      setError('Ошибка. Пожалуйста, попробуйте позже');
    }
  };
  return ( 
      <div className='login-form'>  
        <form onSubmit={handleSubmit}>
          <div>
            
            <div className='input-group'>
              <input
                type="text"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                placeholder='Логин'
              />
            </div>
          </div>
          <div>
            <div className='input-group'>
              <input
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                placeholder='Пароль'
              />
            </div>
          </div>
          <button type="submit" disabled={loading} className='input-group'>
            {loading ? 'Входим...' : 'Вход'}
          </button>
          <button onClick={handlerClick} disabled={loading} className='input-group'>
            {loading ? 'Входим...' : 'Вход по Биометрии'}
          </button>
          {error && <p className='error' style={{ color: 'red' }}>{error}</p>}
        </form>
        <a className="signup-link" href='/register'>Регистрация</a>
        
      </div>
  );
}

export default Login;

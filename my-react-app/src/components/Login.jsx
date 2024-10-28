import  { useState } from 'react';
import { useNavigate } from "react-router-dom";
import '../login.css';
import config from '../config';
// import Register from './Register';

function Login() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const navigate = useNavigate();

  const validateForm = () => {
    if (!username || !password) {
      setError('Username and password are required');
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
        navigate('/home');
      } else {
        const errorData = await response.json();
        setError(errorData.detail || 'Authentication failed!');
      }
    } catch (error) {
      setLoading(false);
      setError('An error occurred. Please try again later.');
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
                placeholder='Username'
              />
            </div>
          </div>
          <div>
            <div className='input-group'>
              <input
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                placeholder='Password'
              />
            </div>
          </div>
          <button type="submit" disabled={loading} className='input-group'>
            {loading ? 'Logging in...' : 'Login'}
          </button>
          {error && <p className='error' style={{ color: 'red' }}>{error}</p>}
        </form>
        <a className="signup-link" href='/register'>Sign up</a>
        
      </div>
  );
}

export default Login;

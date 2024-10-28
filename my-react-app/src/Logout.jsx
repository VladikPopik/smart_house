// import {useState} from 'react';
import { useNavigate } from 'react-router-dom';
// import MyFunctions from './MyFunctions';
// import { Button } from '@mui/material';

function Logout () {
  const navigate = useNavigate();
  const handleLogout = () => {
    localStorage.removeItem('token');
    navigate('/login');
  };

  handleLogout();
}

export default Logout;
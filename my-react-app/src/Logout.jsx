import { useNavigate } from 'react-router-dom';

function Logout () {
  const navigate = useNavigate();
  const handleLogout = () => {
    localStorage.removeItem('token');
    navigate('/login');
  };

  handleLogout();
}

export default Logout;
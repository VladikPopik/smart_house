import  {useEffect} from "react";
import { useNavigate } from 'react-router-dom';
import config from "../config";

export default function Help() {
    const navigate = useNavigate("");
    useEffect(() => {
        const verifyToken = async () => {
          const token = localStorage.getItem('token');
            console.log(token)
          try {
            const response = await fetch(`${config.protocol}://${config.host}:${config.port}/auth/verify-token/${token}`);
    
            if (!response.ok) {
              throw new Error('Token verification failed');
            }
          } catch (error) {
            localStorage.removeItem('token');
            navigate('/login');
          }
        };
        verifyToken();
      }, [navigate]);

      
}
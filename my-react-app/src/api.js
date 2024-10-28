import axios from 'axios';
import config from './config';

const api = axios.create(
    {
        baseURL: `${config.protocol}://${config.host}:${config.port}`,
    }
);

export default api;
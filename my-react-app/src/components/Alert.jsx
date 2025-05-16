import Alert from '@mui/material/Alert';
import CheckIcon from '@mui/icons-material/Check';
import CancelIcon from '@mui/icons-material/Cancel';
import ErrorIcon from '@mui/icons-material/Error';

export default function AlertError ({error, error_code}) {
    if (error_code == 0 && error) {
        return (
        <Alert 
            sx = {
                {
                    position: "absolute",
                    right: 50,
                    top: 825,
                }
            }
            // TODO: Make alerts tomorrow
            icon={<CheckIcon fontSize="inherit" />} severity="success">
            {error && <p className="login" style={{ color: "green", width: "100%"}}>{error}</p>}
        </Alert>);
    }else if (error_code == 1 && error){
        return (
            <Alert 
                sx = {
                    {
                        position: "absolute",
                        right: 50,
                        top: 825,
                    }
                }
                // TODO: Make alerts tomorrow
                icon={<CancelIcon fontSize="inherit" />} severity="error">
                {error && <p className="login" style={{ color: "green", width: "100%"}}>{error}</p>}
            </Alert>);
    } else {
        return (
            <Alert 
                sx = {
                    {
                        position: "absolute",
                        right: 50,
                        top: 825,
                    }
                }
                // TODO: Make alerts tomorrow
                icon={<ErrorIcon fontSize="inherit" />} severity="error">
                {error && <p className="login" style={{ color: "green", width: "100%"}}>{error}</p>}
                {!error && <p className="login" style={{ color: "green", width: "100%"}}>Ошибка системы, проверьте датчик</p>}
        </Alert>);
    }
}
import { Paper, Table, TableBody, TableCell, TableContainer, TableHead, TableRow } from "@mui/material";

import CreateIcon from '@mui/icons-material/Create';
import AddIcon from '@mui/icons-material/Add';
import Button from '@mui/material/Button';
import config from "../config";
import { useEffect, useState, Fragment } from "react";

import TextField from '@mui/material/TextField';
import Dialog from '@mui/material/Dialog';
import DialogActions from '@mui/material/DialogActions';
import DialogContent from '@mui/material/DialogContent';
import DialogContentText from '@mui/material/DialogContentText';
import DialogTitle from '@mui/material/DialogTitle';



async function ReadAllDevices() {
    let values = [];
    try {
        const response = await fetch(
            `${config.protocol}://${config.host}:${config.port}/settings/devices`, {
                method: "GET",
            }
        );
        if (!response.ok) {
          throw new Error('Cannot get devices from server');
        }
        values = await response.json();
        return values;
    } catch (error) {
        console.log(error)
    }
}

async function CreateDevice(props) {
    try {
        const formDetails = new URLSearchParams();
        
        // {props.map( (item, index) => (
        //     formDetails.append(item)    
        // ))}
        
        formDetails.append("device_name", props.device_name)
        formDetails.append("device_type", props.device_type)
        formDetails.append("voltage", props.voltage)
        formDetails.append("pin", props.pin)

        const response = await fetch(
            `${config.protocol}://${config.host}:${config.port}/settings/device`, {
                method: "POST",
                body: formDetails
                // body: JSON.stringify({"device_name": props.device_name, "device_type": props.device_type, "voltage": props.voltage, "pin": props.pin})
            }
        );
        if (!response.ok) {
          throw new Error('Cannot add devices to server');
        }

        return response

    } catch (error) {
        console.log(error)
    }
}

export default function SettingsTable() {

    const [open, setOpen] = useState(false);

    const handleClickOpen = () => {
        setOpen(true);
    };

    const handleClose = () => {
        setOpen(false);
    };

    const [data, setData] = useState([]);

    
    const fetchData = async () => {
        const t_data = await ReadAllDevices();
        setData(t_data);
    }

    window.addEventListener('load', fetchData, false);

    // useEffect(() => {
            
    //     }
    // )



    return (
        <div>
            <TableContainer component={Paper}>
                <Table>
                    <TableHead>
                        <TableRow sx={{display: "flex", alignContent: "center"}}>
                            <TableCell>
                                {/* <Button>
                                    <AddIcon>
                                    </AddIcon>
                                </Button>
                                <Button>
                                    <CreateIcon>
                                        
                                    </CreateIcon>
                                </Button> */}
                                <Fragment>
                                    <Button variant="outlined" onClick={handleClickOpen}>
                                        <AddIcon>
                                            Create device
                                        </AddIcon>
                                    </Button>
                                    <Dialog
                                        open={open}
                                        onClose={handleClose}
                                        PaperProps={{
                                        component: 'form',
                                        onSubmit: (event) => {
                                            event.preventDefault();
                                            const formData = new FormData(event.currentTarget);
                                            const formJson = Object.fromEntries(formData.entries());
                                            const create_device_t = async (props) => {
                                                const response = await CreateDevice(props);
                                            }
                                            create_device_t(formJson);
                                            handleClose();
                                        },
                                        }}
                                    >
                                        <DialogTitle>Create Device</DialogTitle>
                                        <DialogContent>
                                            <DialogContentText>
                                            Please fill fields to add device to your system. 
                                            Be aware that you have to check if pins are the same.
                                            </DialogContentText>
                                            <TextField
                                                autoFocus
                                                required
                                                margin="dense"
                                                id="device_name"
                                                name="device_name"
                                                label="Device Name (8 chars)"
                                                type="string"
                                                fullWidth
                                                variant="standard"
                                            />
                                            <TextField
                                                autoFocus
                                                required
                                                margin="dense"
                                                id="device_type"
                                                name="device_type"
                                                label="Device Type"
                                                type="string"
                                                fullWidth
                                                variant="standard"
                                            />
                                            <TextField
                                                autoFocus
                                                required
                                                margin="dense"
                                                id="voltage"
                                                name="voltage"
                                                label="Device Voltage"
                                                type="float"
                                                fullWidth
                                                variant="standard"
                                            />
                                            <TextField
                                                autoFocus
                                                required
                                                margin="dense"
                                                id="pin"
                                                name="pin"
                                                label="Device PIN number"
                                                type="number"
                                                fullWidth
                                                variant="standard"
                                            />
                                        </DialogContent>
                                        <DialogActions>
                                        <Button onClick={handleClose}>Cancel</Button>
                                        <Button type="submit">Add</Button>
                                        </DialogActions>
                                    </Dialog>
                                    </Fragment>
                            </TableCell>
                        </TableRow>
                        <TableRow>
                            <TableCell>
                                Device name
                            </TableCell>
                            <TableCell>
                                Voltage (V)
                            </TableCell>
                            <TableCell>
                                DeviceType
                            </TableCell>
                            <TableCell>
                                Pin Number
                            </TableCell>
                        </TableRow>
                    </TableHead>
                <TableBody>
                    {data?.map( (item, index) => (
                    <TableRow key={index}>
                        <TableCell>{item.device_name}</TableCell>
                        <TableCell>{item.device_type}</TableCell>
                        <TableCell>{item.voltage}</TableCell>
                        <TableCell>{item.pin}</TableCell>
                    </TableRow>))}
                </TableBody>
                </Table>
            
            </TableContainer>
        </div>
    )
}
import { duration, Paper, Switch, Table, TableBody, TableCell, TableContainer, TableHead, TableRow } from "@mui/material";

import CreateIcon from '@mui/icons-material/Create';
import AddIcon from '@mui/icons-material/Add';
import DeleteIcon from '@mui/icons-material/Delete';
import CheckIcon from '@mui/icons-material/Check';
import Button from '@mui/material/Button';
import config from "../config";
import { useEffect, useState, Fragment } from "react";

import TextField from '@mui/material/TextField';
import Dialog from '@mui/material/Dialog';
import DialogActions from '@mui/material/DialogActions';
import DialogContent from '@mui/material/DialogContent';
import DialogContentText from '@mui/material/DialogContentText';
import DialogTitle from '@mui/material/DialogTitle';
import FormControlLabel from '@mui/material/FormControlLabel';
import Select from '@mui/material/Select';
import MenuItem from '@mui/material/MenuItem';

const sleep = ms => new Promise(r => setTimeout(r, ms));


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
        const response = await fetch(
            `${config.protocol}://${config.host}:${config.port}/settings/device`, {
                method: "POST",
                // body: formDetails
                body: JSON.stringify(
                    {
                        "device_name": props.device_name,
                        "device_type": props.device_type,
                        "voltage": props.voltage, 
                        "pin": props.pin
                    }
                )
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

async function UpdateDevice(props){
    try {
        const response = await fetch(
            `${config.protocol}://${config.host}:${config.port}/settings/device`, {
                method: "PATCH",
                body: JSON.stringify(
                    {
                        "device_name": props.device_name,
                        "device_type": props.device_type,
                        "voltage": props.voltage, 
                        "pin": props.pin,
                        "on": props.on
                    }
                )
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

async function DeleteDevice(device_name){
    try {
        const response = await fetch(
            `${config.protocol}://${config.host}:${config.port}/settings/device?device_name=${device_name}`, {
                method: "DELETE",
            }
        );
        if (!response.ok) {
          throw new Error('Cannot delete device from server');
        }
        
        return response

    } catch (error) {
        console.log(error)
    }
}

export default function SettingsTable() {
    const [toReload, setToReload] = useState(false);
    const [open, setOpen] = useState(false);
    const [updateOpen, SetUpdateOpen] = useState(false);
    const [deviceType, SetDeviceType] = useState('cam');

    const handleClickOpen = () => {
        setOpen(true);
    };

    const handleDeleteDevice = async (device_name) => {
        await DeleteDevice(device_name);
    };

    const handleClose = () => {
        setOpen(false);
    };

    const handleClickUpdateOpen = () => {
        SetUpdateOpen(true);
    };
    const handleCloseUpdate = () => {
        SetUpdateOpen(false);
    }

    const handleOnClick = async (event, item) => {
        {
            // TODO: Fix bug with async message in beetween camera capture
            item.on = !item.on
            await UpdateDevice(item) //JSON.stringify(item)
            setToReload(!toReload);
        }
    }

    const handleChangeDeviceType = (event) => {
        SetDeviceType(event.target.value);
    }

    const [data, setData] = useState([]);

    const fetchData = async () => {
        const t_data = await ReadAllDevices();
        setData(t_data);
    }

    useEffect(() => {
        fetchData();
    }, [toReload])

    let naming_type_hash = {
        "cam": "Camera",
        "dht11": "Climate"
    }

    return (
            <TableContainer component={Paper} sx={{position: "absolute", top: 150, left: 0, width: "75%", height: "75%"}}>
                <Table>
                    <TableHead sx={{}}>
                        <TableRow sx={{display: "flex", alignContent: "center", justifyContent: "center"}}>
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
                            <TableCell sx={{position: "relative", marginLeft: 150}}>
                                <Fragment >
                                    <Button variant="text" onClick={handleClickOpen}>
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
                                            formData.append("device_type", deviceType)
                                            const formJson = Object.fromEntries(formData.entries());
                                            const create_device_t = async (props) => {
                                                const response = await CreateDevice(props);
                                            }
                                            create_device_t(formJson);
                                            handleClose();
                                            setToReload(!toReload);
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
                                            <Select
                                                labelId="device_type"
                                                id="device_type"
                                                value={deviceType}
                                                label="Device Type"
                                                sx={{width: "50%", marginTop: 3}}
                                                onChange={handleChangeDeviceType}
                                            >
                                                <MenuItem value={"cam"}>Camera</MenuItem>
                                                <MenuItem value={"dht11"}>Climate</MenuItem>
                                            </Select>
                                        </DialogContent>
                                        <DialogActions>
                                        <Button onClick={handleClose}>Cancel</Button>
                                        <Button type="submit">Add</Button>
                                        </DialogActions>
                                    </Dialog>
                                </Fragment>
                            </TableCell>
                            
                        </TableRow>
                    </TableHead>
                <TableBody>
                    {data?.map( (item, index) => (
                    <TableRow key={index}>
                        <TableCell>{item.device_name}</TableCell>
                        <TableCell>{item.voltage}</TableCell>
                        <TableCell>{naming_type_hash[item.device_type]}</TableCell>
                        <TableCell>{item.pin}</TableCell>
                        <TableCell>
                        <FormControlLabel
                            value="end"
                            control={
                            <Switch 
                            color="primary"
                            onChange={async (event) => handleOnClick(event, item)}
                            checked={item.on}
                            // disabled={isDisabled(0, 2000)}
                            // checkedIcon={<CheckIcon></CheckIcon>}
                            />}
                            label="Active"
                            labelPlacement="end"
                            />
                        </TableCell>
                        <TableCell>
                            <Fragment>
                                <Button variant="text" onClick={handleClickUpdateOpen}>
                                    <CreateIcon>
                                        Create device
                                    </CreateIcon>
                                </Button>
                                <Dialog
                                    open={updateOpen}
                                    onClose={handleClose}
                                    PaperProps={{
                                    component: 'form',
                                    onSubmit: (event) => {
                                        event.preventDefault();
                                        const formData = new FormData(event.currentTarget);
                                        formData.append('device_name', item.device_name);
                                        formData.append('device_type', deviceType)
                                        const formJson = Object.fromEntries(formData.entries());
                                        const create_device_t = async (props) => {
                                            const response = await UpdateDevice(props);
                                        }
                                        create_device_t(formJson);
                                        handleCloseUpdate();
                                        setToReload(!toReload);
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
                                        <Select
                                                labelId="device_type"
                                                id="device_type"
                                                value={deviceType}
                                                label="Device Type"
                                                sx={{width: "50%", marginTop: 3}}
                                                onChange={handleChangeDeviceType}
                                            >
                                                <MenuItem value={"cam"}>Camera</MenuItem>
                                                <MenuItem value={"dht11"}>Climate</MenuItem>
                                            </Select>
                                    </DialogContent>
                                    <DialogActions>
                                    <Button onClick={handleCloseUpdate}>Cancel</Button>
                                    <Button type="submit">Add</Button>
                                    </DialogActions>
                                </Dialog>
                            </Fragment>
                        </TableCell>
                        <TableCell>
                            <Button onClick={() => {
                                handleDeleteDevice(item.device_name)
                                setToReload(!toReload)
                            } }> 
                                <DeleteIcon>
                                </DeleteIcon>
                            </Button>
                        </TableCell>
                    </TableRow>))}
                </TableBody>
                </Table>
            </TableContainer>
    )
}
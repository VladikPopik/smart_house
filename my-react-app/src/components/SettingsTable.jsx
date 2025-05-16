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
          throw new Error('Невозможно прочитать устройства с сервера');
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
          throw new Error('Невозможно зарегистрировать устройство');
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
          throw new Error('Невозможно зарегистрировать устройство');
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
          throw new Error('Невозможно удалить устройство');
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
        "cam": "Камера",
        "dht11": "Климатический датчик",
        "photoel": "Фото резистор"
    }

    return (
            <TableContainer component={Paper} sx={{position: "absolute", top: 150, left: 50, width: "50%", height: "75%"}}>
                <Table>
                    <TableHead sx={{}}>
                        <TableRow sx={{display: "flex", alignContent: "center", justifyContent: "center"}}>
                        </TableRow>
                        <TableRow>
                            <TableCell>
                                Имя устройства (уникальное)
                            </TableCell>
                            <TableCell>
                                Питание
                            </TableCell>
                            <TableCell>
                                Тип устройства
                            </TableCell>
                            <TableCell>
                                Номер пина на плате
                            </TableCell>
                            <TableCell sx={{position: "relative", marginLeft: 150}}>
                                <Fragment >
                                    <Button variant="text" onClick={handleClickOpen}>
                                        <AddIcon>
                                            Создать устройство
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
                                        <DialogTitle>Добавление устройства</DialogTitle>
                                        <DialogContent>
                                            <DialogContentText>
                                            Пожалуйста заполните все поля чтобы добавить устройство. 
                                            Будьте внимательны с номером пина (должен совпадать с физическим).
                                            </DialogContentText>
                                            <TextField
                                                autoFocus
                                                required
                                                margin="dense"
                                                id="device_name"
                                                name="device_name"
                                                label="Имя устройства (8 символов)"
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
                                                label="Питание устройства"
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
                                                label="PIN номер устройства"
                                                type="number"
                                                fullWidth
                                                variant="standard"
                                            />
                                            <Select
                                                labelId="device_type"
                                                id="device_type"
                                                value={deviceType}
                                                label="Тип устройства"
                                                sx={{width: "50%", marginTop: 3}}
                                                onChange={handleChangeDeviceType}
                                            >
                                                <MenuItem value={"cam"}>Камера</MenuItem>
                                                <MenuItem value={"dht11"}>Климатический датчик</MenuItem>
                                                <MenuItem value={"photoel"}>Фото резистор</MenuItem>
                                            </Select>
                                        </DialogContent>
                                        <DialogActions>
                                        <Button onClick={handleClose}>Отмена</Button>
                                        <Button type="submit">Добавить</Button>
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
                            />}
                            label="Включен"
                            labelPlacement="end"
                            />
                        </TableCell>
                        <TableCell>
                            <Fragment>
                                <Button variant="text" onClick={handleClickUpdateOpen}>
                                    <CreateIcon>
                                        Обновление устройства
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
                                    <DialogTitle>Обновление устройства</DialogTitle>
                                    <DialogContent>
                                        <DialogContentText>
                                        Пожалуйста заполните все поля чтобы добавить устройство. 
                                        Будьте внимательны с номером пина (должен совпадать с физическим).
                                        </DialogContentText>
                                        <TextField
                                            autoFocus
                                            required
                                            margin="dense"
                                            id="voltage"
                                            name="voltage"
                                            label="Питание устройства"
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
                                            label="PIN номер устройства"
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
                                                <MenuItem value={"cam"}>Камера</MenuItem>
                                                <MenuItem value={"dht11"}>Климатический датчик</MenuItem>
                                                <MenuItem value={"photoel"}>Фото резистор</MenuItem>

                                            </Select>
                                    </DialogContent>
                                    <DialogActions>
                                    <Button onClick={handleCloseUpdate}>Отмена</Button>
                                    <Button type="submit">Добавить</Button>
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
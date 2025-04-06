use super::dht::{Dht11, DhtResult};
use serde::{Deserialize, Serialize};

#[derive(Serialize, Deserialize, Debug, Default, Clone)]
pub struct DeviceInfo {
    pub device_name: String,
    pub device_type: String,
    pub(crate) voltage: f32,
    pub(crate) pin: i8,
    pub on: bool,
}

pub struct DhtDevice {
    info: DeviceInfo,
    device: Dht11,
}

#[derive(Clone, Copy)]
pub struct CameraResult;

pub union DevicesResults<T: Copy> {
    pub result: T
}

impl DhtDevice {
    pub fn new(info: DeviceInfo) -> DhtDevice {
        let device = Dht11::new(info.pin.try_into().unwrap());
        DhtDevice {
            info: info,
            device: device,
        }
    }

    pub fn read(&mut self) -> DhtResult {
        self.device.get_reading()
    }

    pub fn get_info(&self) -> DeviceInfo {
        self.info.clone()
    }
}

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

#[derive(Serialize, Deserialize, Debug, Clone, Copy)]
pub struct CameraResult;

#[derive(Clone)]
pub enum DevicesResults {
    DhtResult(f32, f32, DeviceInfo),
}

impl DhtDevice {
    pub fn new(info: DeviceInfo) -> DhtDevice {
        let device = Dht11::new(info.pin.try_into().unwrap());
        DhtDevice { info, device }
    }

    pub fn read(&mut self) -> DhtResult {
        //TODO: for PC!
        // self.device.get_reading()
        DhtResult {
            temperature: 5.0,
            humidity: 5.0,
        }
    }

    pub fn get_info(&self) -> DeviceInfo {
        self.info.clone()
    }
}

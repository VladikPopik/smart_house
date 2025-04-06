use std::collections::HashMap;
use std::env;
use std::time::SystemTime;

use log::{info, warn};
use reqwest::{Response, StatusCode};
use tokio::time::{sleep, Duration};
pub mod devices;
use devices::{
    device::{DeviceInfo, DevicesResults, DhtDevice},
    dht::DhtResult,
};
use rdkafka;

enum Devices {
    dht = 1,
}

async fn get_registered_device(timeout: u8) -> Vec<DeviceInfo> {
    let client = reqwest::Client::new();

    loop {
        sleep(Duration::from_secs(timeout.try_into().unwrap())).await;
        let response: Response = client
            .get("http://backend:8001/settings/devices")
            .send()
            .await
            .unwrap();
        let devices;
        if response.status() == StatusCode::OK {
            devices = response.json::<Vec<DeviceInfo>>().await.unwrap();
            info!("Devices read ===== {:?}", devices);
            return devices;
        }
        sleep(Duration::from_secs(timeout.try_into().unwrap())).await;
        warn!("Error while get request");
    }
}

fn curr_time() -> Duration {
    SystemTime::now()
        .duration_since(SystemTime::UNIX_EPOCH)
        .unwrap()
}

fn perform_device(device_type: Devices, info: DeviceInfo) -> DevicesResults {
    let mut device;
    match device_type {
        Devices::dht => device = DhtDevice::new(info),
        _ => todo!("NOT IMPLEMENTED YET"),
    }
    devices::device::DevicesResults { result: device.read() }
}

pub async fn cycle() {
    dotenv::from_path("./.env").expect("Error loading env, please check if it is okay");
    let time_to_cycle: u8 = env::var("TIME_TO_CYCLE").unwrap().as_str().parse().unwrap();
    let http_timeout: u8 = env::var("HTTP_TIMEOUT").unwrap().as_str().parse().unwrap();
    println!(
        "TIME TO CYCLE = {}, HTTP TIMEOUT = {}",
        time_to_cycle, http_timeout
    );

    let mut connected_devices: HashMap<String, DeviceInfo> = HashMap::new();

    loop {
        let start = curr_time();
        for device in get_registered_device(http_timeout).await.iter() {
            let parse_device = device.to_owned();
            if parse_device.on == true {
                connected_devices.insert(parse_device.device_name.clone(), parse_device);
            }
        }
        println!("Got {:#?}", connected_devices);

        let mut results: Vec<DevicesResults> = vec![];
        for (key, item) in connected_devices.clone().into_iter() {
            rayon::scope(|s| {
                s.spawn(|_| {
                    let device_enum_type;

                    match item.device_type.as_str() {
                        "dht" => device_enum_type = Devices::dht,
                        _ => todo!(),
                    }
                    let result = perform_device(device_enum_type, item);
                    results.push(result);
                });
            });
        }
        //...

        let end = curr_time();
        info!("Cycled elapsed with {:?}", end - start)
    }
}

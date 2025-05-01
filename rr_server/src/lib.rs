use std::collections::HashMap;
use std::env;
use std::time::SystemTime;

use log::{info, warn};
use reqwest::StatusCode;
use tokio::time::{sleep, Duration};
pub mod devices;
use devices::{
    device::{DeviceInfo, DevicesResults, DhtDevice},
    dht::DhtResult,
};
use rdkafka::{
    self,
    producer::{FutureProducer, FutureRecord},
    ClientConfig,
};

enum Devices {
    DHT = 1,
}

struct EnvParams {
    _time_to_cycle: u8,
    http_timeout: u8,
}

async fn get_registered_device(timeout: u8) -> Vec<DeviceInfo> {
    let client = reqwest::Client::new();

    loop {
        sleep(Duration::from_secs(timeout.into())).await;
        let response = client
            .get("http://backend:8001/settings/devices")
            .send()
            .await;

        let parsed_response = match response {
            Ok(_) => response.unwrap(),
            Err(_) => panic!("CANNOT FETCH URL"),
        };

        let devices;
        if parsed_response.status() == StatusCode::OK {
            devices = parsed_response.json::<Vec<DeviceInfo>>().await.unwrap();
            info!("Devices read ===== {:?}", devices);
            return devices;
        }
        sleep(Duration::from_secs(timeout.into())).await;
        warn!("Error while get request");
    }
}

fn curr_time() -> Duration {
    SystemTime::now()
        .duration_since(SystemTime::UNIX_EPOCH)
        .unwrap()
}

fn perform_device(device_type: Devices, info: DeviceInfo) -> DevicesResults {
    let mut device = match device_type {
        Devices::DHT => DhtDevice::new(info),
        _ => todo!("NOT IMPLEMENTED YET"),
    };

    let device_result = match device_type {
        Devices::DHT => device.read(),
        _ => todo!("NOT IMPLEMENTED YET"),
    };

    match device_result {
        DhtResult {
            temperature: temp,
            humidity: hum,
        } => DevicesResults::DhtResult(temp, hum, device.get_info()),
        _ => todo!("NOT IMPLEMENTED YET"),
    }
}

async fn tick(
    connected_devices: &mut HashMap<String, DeviceInfo>,
    env_params: &EnvParams,
) -> (HashMap<String, DevicesResults>, Duration) {
    let start = curr_time();
    for device in get_registered_device(env_params.http_timeout).await.iter() {
        let parse_device = device.to_owned();
        if parse_device.on {
            connected_devices.insert(parse_device.device_name.clone(), parse_device);
        }
    }
    println!("Got {:#?}", connected_devices);

    let mut results: HashMap<String, DevicesResults> = HashMap::new();
    for (_key, item) in connected_devices.clone().into_iter() {
        rayon::scope(|s| {
            s.spawn(|_| {
                let device_enum_type = match item.device_type.as_str() {
                    "dht" => Devices::DHT,
                    _ => todo!(),
                };
                let result = perform_device(device_enum_type, item);
                results.insert(_key, result);
            });
        });
    }
    let end = curr_time();
    let tick_rate = end - start;
    (results, tick_rate)
}

fn read_env(path: String) -> EnvParams {
    dotenv::from_path(path).expect("Error loading env, please check if it is okay");
    let _time_to_cycle: u8 = env::var("TIME_TO_CYCLE").unwrap().as_str().parse().unwrap();
    let http_timeout: u8 = env::var("HTTP_TIMEOUT").unwrap().as_str().parse().unwrap();

    info!(
        "TIME TO CYCLE = {}, HTTP TIMEOUT = {}",
        _time_to_cycle, http_timeout
    );

    EnvParams {
        _time_to_cycle,
        http_timeout,
    }
}

async fn produce(results: HashMap<String, DevicesResults>) {
    let producer: FutureProducer = ClientConfig::new()
        .set("bootstrap.servers", "kafka:9092")
        .create()
        .unwrap();

    for (_k, v) in results.into_iter() {
        match v {
            DevicesResults::DhtResult(temp, hum, info) => {
                let topic = &(info.device_name.to_owned() + &info.device_type.to_owned() + "-rasp");
                let payload: Vec<u8> = vec![temp as u8, hum as u8, 1.0 as u8];
                let _ = producer
                    .send(
                        FutureRecord::to(topic).payload(&payload).key("result"),
                        Duration::new(0, 0),
                    )
                    .await;
            }
            _ => todo!(""),
        }
    }
}

pub async fn cycle() {
    let env_params = read_env("./.env".to_string());

    let mut connected_devices: HashMap<String, DeviceInfo> = HashMap::new();
    loop {
        let (
            results,
            tick_rate
        ) = tick(&mut connected_devices, &env_params).await;
        produce(results).await;
        info!("Tick elapsed with {:?}", tick_rate);
    }
}

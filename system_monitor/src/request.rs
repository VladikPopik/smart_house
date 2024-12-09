use reqwest::blocking::Client;
use serde_json::{from_str, Value};

pub fn request_service(client: &Client) -> u32 {
    let response = client
    .get("http://localhost:8001/system/pid")
    .send().unwrap().text();

    let for_print: Value = from_str(&response.unwrap()).unwrap();

    let pid: u32 = for_print.get("pid").unwrap().as_u64().unwrap() as u32;

    println!("=> pid of backend service: {}", pid);
    pid
}
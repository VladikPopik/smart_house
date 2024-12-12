use std::thread::sleep;
use std::time;
use reqwest::blocking::Client;
use sysinfo::System;

pub mod request;
pub mod system;


// fn main(){
//     //TODO @<VladikPopik>: Add docker file and docker compose
//     println!("@@@@@@@@@@@@@@@@@@@@ START UP @@@@@@@@@@@@@@@@@@@@");
    
//     let mut sys = System::new_all();
//     let client = Client::new();

//     loop {
//         let pid = request::request_service(&client);
        
//         system::system_read(&mut sys, pid);
//         // system::fetch_container_metrics();
//         println!("@@@@@@@@@@@@@@@@@@@@ STEP @@@@@@@@@@@@@@@@@@@@");
//         sleep(time::Duration::new(10, 0));
//     }
// }
// 321652

extern crate rs_docker;

use rs_docker::Docker;

fn main() {
    let mut docker = match Docker::connect("unix:///var/run/docker.sock") {
    	Ok(docker) => docker,
        Err(e) => { panic!("{}", e); }
    };

    let containers = match docker.get_containers(false) {
        Ok(containers) => containers,
        Err(e) => { panic!("{}", e); }
    };

    let stats = match docker.get_stats(&containers[0]) {
        Ok(stats) => stats,
        Err(e) => { panic!("{}", e); }
    };
}
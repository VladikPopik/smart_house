use std::{thread::sleep, time};
use sysinfo::System;
use clap::Parser;
pub mod system;
// pub mod kafka_funcs;
#[derive(Parser, Debug)]
#[command(version, about, long_about = None)]
struct Args {
    #[arg(short, long)]
    pid: u32,
    #[arg(long)]
    topic: String,
    #[arg(long)]
    host: String,
}

#[derive(Debug)]
struct ManagerLoad {
    memory: u64,
    cpu_usage: f32
}

fn now() -> time::Duration {
    let start = std::time::SystemTime::now();
    start.duration_since(std::time::UNIX_EPOCH).expect("Time went backwards")
}

fn main(){
    //TODO @<VladikPopik>: Add docker file and docker compose
    println!("Monitor Manager START UP");

    let args = Args::parse();
    let pid = args.pid;
    // let topic = args.topic;
    // let host = args.host;

    let mut sys = System::new_all();
    loop {
        let start = now();
        println!("===================================================");
        let params = system::system_read(&mut sys, pid);

        let manager_load = ManagerLoad { memory: params.0, cpu_usage: params.1};

        println!("  --  Memory of manager service is {:?} (MB)", (
                manager_load.memory / 1024 / 1024 / 8
            ) as f64
        );
        println!("  --  Memory percent of manager service is {:?}%", (
                manager_load.memory / params.2
            )
        );
        println!("  --  CPU USAGE of manager service is {:?} %",
            manager_load.cpu_usage
        );

        // let max_width = std::cmp::min(
        //     1000.0, 
        //     1000.0 * manager_load.cpu_usage * (manager_load.memory as f32 / params.2 as f32 / 4 as f32)
        // );

        system::downscale_image(
            "/pics/image.png",
            "/pics/image_test.png",
            1000.0,
            "lcz3"
        );
        let end = now();
        // kafka_funcs::consumer(topic, host);
        println!("Cycle elapsed with: {:?}", end - start);
        sleep(time::Duration::new(5, 0));
    }
}
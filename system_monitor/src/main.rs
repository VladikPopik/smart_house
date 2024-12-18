use std::thread::sleep;
use std::time;
use sysinfo::System;
use clap::Parser;
pub mod system;

#[derive(Parser, Debug)]
#[command(version, about, long_about = None)]
struct Args {
    #[arg(short, long)]
    pid: u32,
    #[arg(long)]
    topic: String,
    #[arg(long)]
    host: String
}

#[derive(Debug)]
struct ManagerLoad {
    memory: u64,
    cpu_usage: f32
}

fn main(){
    //TODO @<VladikPopik>: Add docker file and docker compose
    println!("Monitor Manager START UP");

    let args = Args::parse();
    let pid = args.pid;
    let topic = args.topic;
    let host = args.host;

    let mut sys = System::new_all();
    loop {
        println!("===================================================");
        let params = system::system_read(&mut sys, pid);

        let manager_load = ManagerLoad { memory: params.0, cpu_usage: params.1};

        println!("  --  Memory of manager service is {:?} (MB)", (
            manager_load.memory / 1024 / 1024 / 8) as f64
        );
        println!("  --  CPU USAGE of manager service is {:?} %",
            manager_load.cpu_usage
        );

        sleep(time::Duration::new(10, 0));
    }
}
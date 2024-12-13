use std::thread::sleep;
use std::process::Command;
use std::time;
use sysinfo::System;
use clap::Parser;
pub mod system;

#[derive(Parser, Debug)]
#[command(version, about, long_about = None)]
struct Args {
    #[arg(short, long)]
    pid: u32,
}

fn main(){
    //TODO @<VladikPopik>: Add docker file and docker compose
    println!("@@@@@@@@@@@@@@@@@@@@ START UP @@@@@@@@@@@@@@@@@@@@");

    let args = Args::parse();
    let pid = args.pid;

    let mut sys = System::new_all();
    loop {
        system::system_read(&mut sys, pid);
        println!("@@@@@@@@@@@@@@@@@@@@ STEP @@@@@@@@@@@@@@@@@@@@");
        sleep(time::Duration::new(10, 0));

    }

    // let output = Command::new("ps")
    // .output()
    // .expect("Failed to execute command");

    // // assert_eq!(b"Hello world\n", output.stdout.as_slice());
    // println!("{:?}", output.stdout.as_slice());

}
// 59656
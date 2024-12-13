use sysinfo::{System, Pid};

pub fn system_read(sys: &mut System, pid: u32) -> (u64, f32){
    sys.refresh_all();

    println!("=> system:");
    // RAM and swap information:
    println!("total memory: {} bytes", sys.total_memory());
    println!("used memory : {} bytes", sys.used_memory());

    // Display system information:
    println!("System name:             {:?}", System::name());
    println!("System kernel version:   {:?}", System::kernel_version());
    println!("System OS version:       {:?}", System::os_version());
    println!("System host name:        {:?}", System::host_name());

    // Number of CPUs:
    println!("NB CPUs: {}", sys.cpus().len());

    let manager_process =  sys.process(Pid::from_u32(pid));

    let manager_memory = manager_process.expect("No process").memory();
    let manager_cpu_usage = manager_process.expect("No process").cpu_usage()/(sys.cpus().len() as f32);

    println!("{:?} bytes", manager_memory);
    println!("{:?} %", manager_cpu_usage);

    (manager_memory, manager_cpu_usage)

}
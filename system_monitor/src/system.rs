use sysinfo::{System, Pid};

pub fn system_read(sys: &mut System, pid: u32) -> (u64, f32){
    sys.refresh_all();

    println!("=> system:");
    // RAM and swap information:
    println!("  --  total memory: {} bytes", sys.total_memory());
    println!("  --  used memory : {} bytes", sys.used_memory());

    // Display system information:
    println!("  --  System name:             {:?}", System::name().unwrap());
    println!("  --  System kernel version:   {:?}", System::kernel_version().unwrap());
    println!("  --  System OS version:       {:?}", System::os_version().unwrap());
    println!("  --  System host name:        {:?}", System::host_name().unwrap());

    // Number of CPUs:
    println!("  --  NB CPUs: {}", sys.cpus().len());

    println!("=> manager");
    let manager_process =  sys.process(Pid::from_u32(pid));

    let manager_memory = manager_process.expect("No process").memory();
    let manager_cpu_usage = manager_process.expect("No process").cpu_usage()/(sys.cpus().len() as f32);

    (manager_memory, manager_cpu_usage)
}
use sysinfo::{System, Pid};

pub fn system_read(sys: &mut System, pid: u32) {
    sys.refresh_all();

    println!("=> system:");
    // RAM and swap information:
    println!("total memory: {} bytes", sys.total_memory());
    println!("used memory : {} bytes", sys.used_memory());
    println!("total swap  : {} bytes", sys.total_swap());
    println!("used swap   : {} bytes", sys.used_swap());

    // Display system information:
    println!("System name:             {:?}", System::name());
    println!("System kernel version:   {:?}", System::kernel_version());
    println!("System OS version:       {:?}", System::os_version());
    println!("System host name:        {:?}", System::host_name());

    // Number of CPUs:
    println!("NB CPUs: {}", sys.cpus().len());

    // println!("{:?}", sys.process(Pid::from_u32(pid))); // 321652 321629
    println!("{:?}", sys.process(Pid::from_u32(pid)));
}

// pub fn fetch_container_metrics() -> Result<(), Box<dyn std::error::Error>> {
//     let containers = Docker::list_containers();
   
//     for container in containers {
//         let container: Container = docker.inspect_container(&container.id);
   
//         // Fetch specific metrics from the 'container' object
//         // and store them in variables
   
//         println!("Container ID: {}", container.id);
//         println!("Metrics: {:?}", container.metrics());
//         println!("--------------------------");
//     }
   
//     Ok(())
// }
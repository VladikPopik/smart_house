use sysinfo::{System, Pid};

use image::imageops::FilterType;
use image::ImageFormat;

pub fn downscale_image(file_path: &str, output_path: &str, max_width_px: f64, filter_type: &str) {

    let filters = std::collections::HashMap::from(
        [
            ("near", FilterType::Nearest),
            ("tri", FilterType::Triangle),
            ("cmr", FilterType::CatmullRom),
            ("gauss", FilterType::Gaussian),
            ("lcz3", FilterType::Lanczos3)
        ]
    );

    let full_path = std::env::current_dir().unwrap().display().to_string() + file_path;
    let full_output_path = std::env::current_dir().unwrap().display().to_string() + output_path;
    
    let image = image::open(&full_path).unwrap();
    
    let (width, height) = image::GenericImageView::dimensions(&image);
    let ratio: f64 = width as f64 / height as f64;
    let new_height = max_width_px / ratio;

    let new_image = image.resize(
        max_width_px as u32, 
        new_height as u32, 
        *filters.get(filter_type).unwrap()
    );
    // + "_test_" + filter_type
    let format = ImageFormat::from_path(&full_path).unwrap();
    let mut output = std::fs::File::create(full_output_path).unwrap();
    new_image.write_to(&mut output, format).unwrap();

    println!("Picture is downscaled at {:?}", output)

}

pub fn system_read(sys: &mut System, pid: u32) -> (u64, f32, u64){
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
    // Information about Manager:
    let manager_process =  sys.process(Pid::from_u32(pid));

    let manager_memory = manager_process.expect("No process")
        .memory();
    let manager_cpu_usage = manager_process.expect("No process")
        .cpu_usage()/(sys.cpus().len() as f32);

    (manager_memory, manager_cpu_usage, sys.total_memory())
}
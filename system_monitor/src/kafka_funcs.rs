use kafka::consumer::{Consumer, FetchOffset};
use image::RgbImage;
use ndarray::Array3;

fn array_to_image(arr: Array3<u8>) -> RgbImage {
    assert!(arr.is_standard_layout());

    let (height, width, _) = arr.dim();
    let t_raw= arr.into_raw_vec_and_offset();
    let raw = t_raw.0;

    RgbImage::from_raw(width as u32, height as u32, raw)
        .expect("container should have the right size for the image dimensions")
}

fn consumer(topic: String, hosts: String) {
    let hosts = vec![hosts];
 
    let mut consumer = Consumer::from_hosts(hosts)
        .with_topic(topic)
        .with_fallback_offset(FetchOffset::Latest)
        .create()
        .unwrap();

    loop {
        for ms in consumer.poll().unwrap().iter() {
            for m in ms.messages() {
            // If the consumer receives an event, this block is executed
                println!("{:?}", m.value);
            }

            consumer.consume_messageset(ms).unwrap();
        }

        consumer.commit_consumed().unwrap();
    }
}


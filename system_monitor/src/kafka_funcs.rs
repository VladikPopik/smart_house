use kafka::consumer::{Consumer, FetchOffset};
use image::RgbImage;
use ndarray::Array3;

fn array_to_image(arr: Array3<u8>) -> RgbImage {
    assert!(arr.is_standard_layout());

    let (height, width, _) = arr.dim();
    let raw = arr.into_raw_vec();

    RgbImage::from_raw(width as u32, height as u32, raw)
        .expect("container should have the right size for the image dimensions")
}

fn consumer() {
    let hosts = vec!["kafka:9092".to_owned()];
 
    let mut consumer = Consumer::from_hosts(hosts)
        .with_topic("topic-name".to_owned())
        .with_fallback_offset(FetchOffset::Latest)
        .create()
        .unwrap();

    loop {
        for ms in consumer.poll().unwrap().iter() {
            for m in ms.messages() {
            // If the consumer receives an event, this block is executed
                println!("{:?}", str::from_utf8(m.value).unwrap());
            }

            consumer.consume_messageset(ms).unwrap();
        }

        consumer.commit_consumed().unwrap();
    }
}
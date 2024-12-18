use kafka::consumer::{Consumer, FetchOffset};

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
FROM rust:1.85.0-alpine AS builder

# install crates.io index and cache it in the docker layer
RUN cargo new --bin build-index \
  && cd build-index \
  && cargo add rand_core \
  && cd .. \
  && rm -rf build-index

WORKDIR /rr_server

RUN rustup target add x86_64-unknown-linux-musl

COPY . ./
RUN cargo build --target x86_64-unknown-linux-musl

FROM scratch

COPY --from=builder /rr_server/target/x86_64-unknown-linux-musl/release/test /usr/local/bin/test

CMD ["test"]
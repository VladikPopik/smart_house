FROM rust:1.85.0-alpine

RUN apk add --no-cache musl-dev
WORKDIR /rr_server
COPY . ./
RUN cargo build --release

EXPOSE 5000
CMD ["cargo run"]
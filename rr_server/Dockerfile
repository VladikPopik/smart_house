# Use the official Rust image as a build stage
FROM rust:1.85 AS builder

# Set the working directory
WORKDIR /

# Copy the Cargo toml files first to cache dependencies
# COPY Cargo.toml Cargo.lock ./
COPY . .

RUN rustup update
RUN cargo build

# Copy the source code

# # Build the application
# RUN cargo build

# # Use a small image for the final build
# FROM debian:buster-slim

# # Copy the application binary from the builder stage
# COPY --from=builder rr_server/target/debug/rr_server .

# Specify the command to run the application
CMD ["cd src ; cargo run"]
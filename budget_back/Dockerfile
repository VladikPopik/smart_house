FROM rust:1.83.0

WORKDIR /budget
COPY . .

RUN cargo install --path ./budget
RUN cd ./budget
EXPOSE 80
CMD ["./budget"]

# Lite Redis Server

A lightweight, simplified Redis server implementation. Perfect for learning and experimenting with Redis concepts in a minimal setup.

## Features

- **TCP Server with Concurrency Support:** Efficient handling of multiple connections simultaneously.
- **RESP Protocol Support:** Communicates using the Redis Serialization Protocol (RESP).
- **Built with Test-Driven Development (TDD):** Ensuring robust and reliable code through comprehensive testing.
- Basic key-value store
- Minimal dependencies for easy setup
- Supports fundamental Redis commands
- **Supported Commands:**
  - `PING`: Check server responsiveness.
  - `ECHO`: Echo back the given message.
  - `SET`: Set a key to hold the string value.
  - `GET`: Get the value of a key.
  - `EXISTS`: Check if a key exists.
  - `DEL`: Delete a key.
  - `INCR`: Increment the integer value of a key.
  - `DECR`: Decrement the integer value of a key.
  - `LPUSH`: Insert all the specified values at the head of the list.
  - `RPUSH`: Insert all the specified values at the tail of the list.
- **Command Options for `SET`:**
  - `EX`: Set the specified expire time, in seconds.
  - `PX`: Set the specified expire time, in milliseconds.
  - `EXAT`: Set the specified Unix time at which the key will expire, in seconds.
  - `PXAT`: Set the specified Unix time at which the key will expire, in milliseconds.
- **Database Types:**
  - **Normal DB:** Standard key-value store.
  - **TTL-Keys-Supported DB:** Key-value store with support for time-to-live (TTL) keys, running an additional thread to handle key expiration.

## Getting Started

1. **Clone the repository**
    ```sh
    git clone https://github.com/yourusername/lite-redis-server.git
    cd lite-redis-server
    ```

2. **Build and Run**
    ```sh
    python3 -m server.server
    ```

3. **Usage**
    - Connect using any Redis client or `redis-cli`
    - Supported commands: `SET`, `GET`, `DEL`, `EXISTS`, etc.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request.

# **Cafeteria** - A Project to Save Your Time Ordering Coffee

## Overview

Cafeteria is a backend project designed to streamline and simplify the process of ordering coffee, ensuring a faster and more efficient experience for users.

## Technologies Used

- **FastAPI** - High-performance web framework for building APIs.
- **WebSockets** - Real-time communication support.
- **PostgreSQL** - Relational database management system.
- **Redis** - In-memory data structure store for caching and message brokering.
- **Docker** - Containerization platform for easy deployment.

## Running the Project Locally

### 1. Clone the Repository

```bash
    git clone https://github.com/xerottin/cafeteria.git
```

### 2. Install Docker

Ensure you have Docker installed. If not, install it using:

```bash
    pip install docker
```

### 3. Start Docker and Create a Network

```bash
    docker network create cafeteria-network
```

### 4. Build and Run the Docker Container

```bash
    docker compose up --build
```

## Structure of project

http://0.0.0.0:8009/user/docs#/
http://0.0.0.0:8009/admin/docs#/
http://0.0.0.0:8009/cafeteria/docs#/

## Conclusion

Project is now set up for local development and testing! Feel free to customize the Docker configuration and database settings to suit your needs.


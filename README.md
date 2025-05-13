# ☕ **Cafeteria** - Simplifying Your Coffee Ordering Experience

## 🌟 Overview

**Cafeteria** is a robust backend system built to streamline the coffee ordering process. By leveraging cutting-edge technologies, this project ensures users can easily place orders with minimal delay, offering an efficient and enjoyable experience.

---

## 🛠 Technologies Used

* **[FastAPI](https://fastapi.tiangolo.com/)** — High-performance framework for rapid API development.
* **WebSockets** — Real-time, bidirectional communication.
* **PostgreSQL** — Reliable and scalable database system.
* **Redis** — Caching and message-brokering for improved performance.
* **Docker** — Containerization to simplify deployment and testing.

---

## 📦 Project Structure and API Endpoints

The backend provides structured APIs divided into clear segments:

### 📌 User API

* `POST /user/register` – Register new users.
* `POST /user/login` – Authenticate users and provide access tokens.
* `GET /user/profile` – Retrieve user profile information.

**Documentation:** [http://0.0.0.0:8009/user/docs#/](http://0.0.0.0:8009/user/docs#/)

### 🔧 Admin API

* `POST /admin/login` – Admin authentication.
* `GET /admin/orders` – View and manage all orders.
* `PUT /admin/orders/{id}` – Update order status.

**Documentation:** [http://0.0.0.0:8009/admin/docs#/](http://0.0.0.0:8009/admin/docs#/)

### ☕ Cafeteria API

* `GET /cafeteria/menu` – Retrieve current coffee menu.
* `POST /cafeteria/order` – Place new orders.
* `GET /cafeteria/order/{id}` – Check order status.
* `WebSocket /cafeteria/ws/orders` – Real-time order updates.

**Documentation:** [http://0.0.0.0:8009/cafeteria/docs#/](http://0.0.0.0:8009/cafeteria/docs#/)

---

## 🖥 Running the Project Locally

### 1. Clone the Repository

```bash
git clone https://github.com/xerottin/cafeteria.git
```

### 2. Install Docker

Ensure Docker is installed. Download from [Docker](https://www.docker.com/) if needed.

### 3. Create Docker Network

```bash
docker network create cafeteria-network
```

### 4. Build and Run with Docker Compose

```bash
docker compose up --build -d
```

---

## 🚦 Conclusion

You are now ready to develop and test locally! Customize Docker and database configurations to fit your development needs. Happy coding!

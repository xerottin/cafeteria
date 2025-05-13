# ☕ **Cafeteria** - Streamline Your Coffee Ordering Experience

## 🚀 Overview

**Cafeteria** is a robust backend system designed to simplify and accelerate the coffee ordering process. With real-time communication and a clean API structure, users can enjoy an efficient ordering experience.

## 🛠 Technologies Used

* **FastAPI** - Modern, high-performance web framework for APIs.
* **WebSockets** - Real-time bidirectional communication.
* **PostgreSQL** - Reliable relational database management system.
* **Redis** - Fast caching and message brokering.
* **Docker** - Containerization platform for easy deployment.

## 📌 Project Structure and API Endpoints

### 🧑 User API

* `POST /user/register` – Register new users.
* `POST /user/verify` – Verify user account with a verification code.
* `GET /user/profile` – Retrieve user profile information.
* `GET /user/nearby-cafeteria` – Find nearby cafeterias.
* `GET /user/cafeteria/{id}/menu` – Retrieve the menu of a specific cafeteria.
* `GET /user/menu/{id}/coffee` – Retrieve details of a specific coffee.
* `POST /user/order` – Create a new coffee order.
* `GET /user/orders/archive` – Retrieve archive of user orders.
* `POST /user/favourite` – Add items to user's favourites.
* `GET /user/favourites` – Retrieve user's favourite items.

**Documentation:** [http://0.0.0.0:8009/user/docs#/](http://0.0.0.0:8009/user/docs#/)

### ⚙️ Admin API

* `POST /admin/login` – Authenticate admin users.
* `GET /admin/orders` – View and manage all orders.
* `PUT /admin/orders/{id}` – Update the status of an order.
* CRUD operations for managing admins.
* CRUD operations for managing cafeterias.

**Documentation:** [http://0.0.0.0:8009/admin/docs#/](http://0.0.0.0:8009/admin/docs#/)

### ☕ Cafeteria API

* `POST /cafeteria/menu` – Create a new menu.
* `GET /cafeteria/menu/{id}` – Retrieve a specific menu.
* `GET /cafeteria/menus` – Retrieve all menus.
* `POST /cafeteria/coffee` – Create a new coffee item.
* `GET /cafeteria/orders` – Retrieve orders placed by users.
* `GET /cafeteria/orders/{user_id}` – Retrieve orders placed by a specific user.
* `POST /cafeteria/orders/{id}/send` – Send (dispatch) an order to a user.
* `WebSocket /cafeteria/ws/orders` – Real-time updates on orders.

**Documentation:** [http://0.0.0.0:8009/cafeteria/docs#/](http://0.0.0.0:8009/cafeteria/docs#/)

## 🖥 Running the Project Locally

### 1. Clone the Repository

```bash
git clone https://github.com/xerottin/cafeteria.git
```

### 2. Ensure Docker is Installed

Install Docker from the official site if necessary: [Docker](https://www.docker.com/).

### 3. Create a Docker Network

```bash
docker network create cafeteria-network
```

### 4. Build and Run Docker Containers

```bash
docker compose up --build
```

## 🎉 Conclusion

Your local development environment is now ready! Feel free to customize the Docker setup and database configurations as per your needs.

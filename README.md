# E-commerce API

### ---- WORK IN PROGRESS ----

This application was built for educational purposes and is not intended for production use.

## Overview
E-commerce API built with FastAPI.

### Motives
The main reason for creating this application was to learn new technologies 
and build a real-world application from scratch.

Main features:
- Built with `FastAPI`
- Inventory stored in `redis` with async `aredis_om`
- User data in async `mongo db` with `motor`
- User authentication with `oauth2` and JSON web tokens
- Admin endpoints protected with HTTP basic authentication
- Data validation with `HashModel`
- Password hashing with `bcrypt`
- custom error handling
- Slack notification of new orders with async `httpx`

### E-commerce API
E-commerce API allows you to:

- as a user: signup and login to use services
- as a user: make an authorized order
- as admin: perform all basic operations such as create, get, update and delete on:
  - product inventory
  - orders
  - users

### Authentication
As a user you will need signup. To access `/orders` endpoints you will need to login with `Oauth2` and access token.
To access `/admin` endpoints you'll need admin credentials. You can pass them via `HTTPBasicAuth`.

### Dependencies
Dependency management is handled using `requirements.txt` file. 

### Docker setup

1. Build a docker image: `docker build -t ecommerce_api .`
2. Start redis server with : `docker-compose up -d --build --force-recreate ecommerce_api`
3. Create a running container: `docker run -p 80:80 ecommerce_api`

### Local setup

1. Install dependencies from `requirements.txt` file
2. Run the app: `uvicorn ecommerce_api.main:app --reload`

## Documentation
Once the application is up and running, you can access FastAPI automatic docs 
at `/docs` endpoint.

### Admin endpoints

| Method | Endpoint               | Description             |
|--------|------------------------|-------------------------|
| POST   | /products/new          | Create new product      |
| PUT    | /products/{product_id} | Update existing product |
| DELETE | /products/{product_id} | Delete product          |
| GET    | /orders/all            | Get all orders          |
| GET    | /orders/{order_id}     | Get an order            |
| GET    | /users/all             | Get all users           |
| GET    | /users/{email}         | Get user info           |
| DELETE | /users/{email}         | Delete user             |

### User endpoints

| Method | Endpoint               | Description                 |
|--------|------------------------|-----------------------------|
| GET    | /products/all          | Get all products            |
| GET    | /products/{product_id} | Get a product               |
| GET    | /products/{category}   | Search products by category |
| GET    | /products/{name}       | Search products by name     |
| GET    | /orders/{product_id}   | Get order                   |
| POST   | /orders/new            | Create order                |


## Status codes

| Status code | Description                               |
|-------------|-------------------------------------------|
| 200         | success                                   |
| 400         | bad request, please check your request    |
| 401         | user unauthorized                         |
| 404         | not found                                 |
| 424         | external dependency failed                |
| 500         | internal server error, application failed |

## Testing
You can test api with `Postman` and `Insomnia`

# Smart E-Commerce Checkout System

A cloud-based microservices architecture demonstrating a complete e-commerce checkout pipeline using REST APIs, asynchronous messaging, and persistent database storage — without a UI.

---

## Table of Contents

- [Overview](#overview)
- [Architecture](#architecture)
- [Technologies Used](#technologies-used)
- [Project Structure](#project-structure)
- [Prerequisites](#prerequisites)
- [Installation & Setup](#installation--setup)
- [Running the Services](#running-the-services)
- [API Documentation](#api-documentation)
- [Discount Function](#discount-function)
- [RabbitMQ Messaging](#rabbitmq-messaging)
- [Database Verification](#database-verification)
- [Expected Outcomes](#expected-outcomes)
- [Shutdown](#shutdown)

---

## Overview

This project demonstrates the **end-to-end execution** of a Smart E-Commerce Checkout System by connecting individual microservices into a complete checkout pipeline that reflects a real-world e-commerce workflow.

The system includes:
- **Cart Service** — manages shopping cart items
- **Payment Service** — processes payments with or without discount
- **Inventory Service** — tracks stock levels in MySQL database
- **Discount Function** — serverless-style discount code handler
- **RabbitMQ** — asynchronous event messaging between services
- **MySQL** — persistent database for inventory

---

## Architecture

```
┌─────────────────────────────────────────────────────┐
│           Smart E-Commerce Checkout Pipeline         │
│                                                      │
│   [Cart Service]  ──▶  [Discount Function]           │
│        │                      │                      │
│        ▼                      ▼                      │
│  [Payment Service]  ──▶  [Inventory Service]         │
│        │                      │                      │
│        ▼                      ▼                      │
│   [RabbitMQ]             [MySQL Database]            │
└─────────────────────────────────────────────────────┘

Flow: Cart → Discount → Payment → Inventory → RabbitMQ Event
```

---

## Technologies Used

| Technology | Purpose | Version |
|-----------|---------|---------|
| Node.js + Express | Cart Service | 18 |
| Python + Flask | Payment Service | 3.11 |
| Spring Boot + JPA | Inventory Service | 3.1.2 |
| MySQL | Inventory Database | 8 |
| RabbitMQ | Async Messaging | 3 |
| Docker + Compose | Containerization | Latest |
| Postman | API Testing | Latest |

---

## Project Structure

```
smart-ecom/
│
├── cart-service/
│   ├── index.js              # Express REST API
│   ├── package.json          # Node dependencies
│   └── Dockerfile
│
├── payment-service/
│   ├── app.py                # Flask REST API
│   ├── notify.py             # RabbitMQ publisher
│   └── Dockerfile
│
├── inventory-service/
│   ├── src/
│   │   └── main/
│   │       ├── java/com/example/inventory/
│   │       │   ├── InventoryController.java
│   │       │   ├── Stock.java
│   │       │   └── StockRepository.java
│   │       └── resources/
│   │           └── application.properties
│   ├── pom.xml
│   └── Dockerfile
│
├── discount-function/
│   ├── handler.js            # Serverless discount logic
│   └── serverless.yml
│
├── deploy/
│   ├── docker-compose.yml    # Orchestration
│   ├── k8s-cart.yaml
│   └── nginx.conf
│
└── README.md
```

---

## Prerequisites

Make sure the following are installed on your system:

- [Docker Desktop](https://www.docker.com/products/docker-desktop/)
- [Node.js v18+](https://nodejs.org/)
- [Python 3.x](https://www.python.org/)
- [Postman](https://www.postman.com/downloads/)
- pip package: `pika`

```bash
pip install pika
```

---

## Installation & Setup

### Step 1 — Extract the project

```bash
unzip smart-ecom.zip
cd smart-ecom
```

### Step 2 — Verify folder structure

```bash
ls
# cart-service  payment-service  inventory-service  discount-function  deploy
```

---

## Running the Services

### Step 1 — Start all containers

```bash
cd deploy
docker-compose up --build -d
```

### Step 2 — Verify all containers are running

```bash
docker ps
```

Expected output:

```
CONTAINER           PORT     STATUS
deploy-cart-1       3001     Up
deploy-payment-1    3002     Up
deploy-inventory-1  3003     Up
deploy-rabbitmq-1   5672     Up
deploy-mysql-1      3307     Up
```

### Step 3 — Check inventory logs (confirm MySQL connected)

```bash
docker logs deploy-inventory-1 --tail 5
```

Expected:
```
HikariPool-1 - Start completed
Tomcat started on port(s): 3003
Started InventoryMain in 8.715 seconds
```

---

## API Documentation

### 1. Inventory Service — Port 3003

#### POST — Add Inventory Items

```
POST http://localhost:3003/inventory/update
Content-Type: application/json
```

Request Body:
```json
{
  "Laptop": 50,
  "Phone": 100,
  "Headphones": 30
}
```

Response:
```json
[
  {"id": 1, "name": "Laptop", "qty": 50},
  {"id": 2, "name": "Phone", "qty": 100},
  {"id": 3, "name": "Headphones", "qty": 30}
]
```

#### GET — Retrieve All Inventory Items

```
GET http://localhost:3003/inventory/view
```

Response:
```json
[
  {"id": 1, "name": "Laptop", "qty": 50},
  {"id": 2, "name": "Phone", "qty": 100},
  {"id": 3, "name": "Headphones", "qty": 30}
]
```

#### PUT — Update Inventory After Purchase

```
POST http://localhost:3003/inventory/update
Content-Type: application/json
```

Request Body:
```json
{
  "Laptop": 48
}
```

---

### 2. Cart Service — Port 3001

#### POST — Add Item to Cart

```
POST http://localhost:3001/add
Content-Type: application/json
```

Request Body:
```json
{
  "item": {
    "name": "Laptop",
    "price": 999.99,
    "qty": 2
  }
}
```

Response:
```json
{
  "cart": [
    {"name": "Laptop", "price": 999.99, "qty": 2}
  ]
}
```

#### GET — View Cart Contents

```
GET http://localhost:3001/view
```

Response:
```json
{
  "cart": [
    {"name": "Laptop", "price": 999.99, "qty": 2}
  ]
}
```

---

### 3. Payment Service — Port 3002

#### POST — Process Payment WITH Discount

```
POST http://localhost:3002/pay
Content-Type: application/json
```

Request Body:
```json
{
  "amount": 799.99,
  "method": "card",
  "discount_code": "NEWYEAR"
}
```

Response:
```json
{
  "status": "ok",
  "amount": 799.99,
  "method": "card"
}
```

#### POST — Process Payment WITHOUT Discount

```
POST http://localhost:3002/pay
Content-Type: application/json
```

Request Body:
```json
{
  "amount": 999.99,
  "method": "UPI"
}
```

Response:
```json
{
  "status": "ok",
  "amount": 999.99,
  "method": "UPI"
}
```

---

## Discount Function

The discount function runs serverless-style locally using Node.js.

### Run Discount Calculation

```bash
cd discount-function
node -e "
const h = require('./handler');
h.apply({body: JSON.stringify({code: 'NEWYEAR', amount: 999.99})}).then(r => {
  const b = JSON.parse(r.body);
  console.log('Code:           NEWYEAR');
  console.log('Discount Rate:  ' + b.discount * 100 + '%');
  console.log('Original Total: 999.99');
  console.log('Final Total:    ' + (999.99 - (999.99 * b.discount)).toFixed(2));
});
"
```

Output:
```
Code:           NEWYEAR
Discount Rate:  20%
Original Total: 999.99
Final Total:    799.99
```

### Discount Codes

| Code | Discount |
|------|----------|
| NEWYEAR | 20% off |
| Any other | 0% off |

---

## RabbitMQ Messaging

### Step 1 — Open Terminal 1 (Consumer/Listener)

```bash
cd inventory-service
python consumer.py
```

Output:
```
Waiting for events...
```

### Step 2 — Open Terminal 2 (Publisher)

```bash
cd payment-service
python notify.py
```

### Step 3 — Terminal 1 receives the event

```
Waiting for events...
Event: payment_processed
```

### Verify via RabbitMQ Management UI

```
URL:      http://localhost:15672
Username: guest
Password: guest
```

Navigate to **Queues** tab → click `events` queue → **Get Messages**

---

## Database Verification

### Connect to MySQL

```bash
docker exec -it deploy-mysql-1 mysql -u root -psecret inventory
```

### Query inventory table

```sql
SELECT * FROM stock;
```

Output:
```
+----+------------+-----+
| id | name       | qty |
+----+------------+-----+
|  1 | Laptop     |  50 |
|  2 | Phone      | 100 |
|  3 | Headphones |  30 |
|  4 | Laptop     |  48 |
+----+------------+-----+
```

### Exit MySQL

```sql
EXIT;
```

---

## Expected Outcomes

### 1. Checkout Choreography via Postman
```
Cart → Discount → Payment → Inventory
```

### 2. System Resilience
- Inventory updates **persist in MySQL** even after container restart
- RabbitMQ `events` queue confirms **asynchronous communication**

### 3. Real-World Workflow
- Mimics **Amazon/Flipkart** checkout pipeline
- Cart, Payment, and Inventory are **independent but coordinated** services
- Demonstrates **synchronous REST** and **asynchronous messaging**

---

## Shutdown

```bash
cd deploy
docker-compose down
```

---

## Author

**Course:** MCA Semester 2 — Advanced Cloud Computing
**Project:** Smart E-Commerce Checkout System
**Description:** Microservices-based checkout pipeline using Docker, RabbitMQ, MySQL, Node.js, Python, and Spring Boot

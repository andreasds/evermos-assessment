# Online Store 12.12 Event

## Problem happened

* Lost handling when the order is bigger than the current stock
* Unhandled usage of shared resources (current stock value at this case)
  when used at the same time (race condition)

## Solution offered

* Put a lock around the shared data to ensure only one thread can access
  the data at a time

## Requirements

* [Docker](https://docs.docker.com/get-docker/) Docker Engine
* [MySQL](https://www.mysql.com) MySQL Database
* [Python](https://www.python.org/downloads) Python programming language
* [Flask](https://flask.palletsprojects.com/en/1.1.x/) Micro web framework
* [MySQL Connector](https://dev.mysql.com/downloads/connector/python/) MySQL driver

## Setup

```bash
./scripts/setup-dev.sh
```

From that script, we have:

* Database run at port 17306 with root password `mysql-admin`
* Backend run with API access port 18001

## How to Run

```bash
./scripts/run.sh
```

* API Endpoint will run at http://localhost:18001/

## How to Run manually

```bash
python -m online_store --conf configs/online-store.conf
```

## Postman Collection

* [Postman Collection](configs/evermos_postman.json)

## API Endpoint

### Customer

* Add Customer, create new customer

```json
POST /customer/add
{
  "username": "customer1"
}
```

### Product

* Get All Products, fetch all products

```json
GET /product/all
```

* Get Product, collect product detail

```json
GET /product/<product_id>
```

* Add Product, create new product

```json
POST /product/add
{
  "product_name": "product1",
  "stock": 0
}
```

* Update Product Stock, update product stock

```json
POST /product/add-stock
{
  "product_id": "product1",
  "stock": 10
}
```

### Cart

* Get Cart, collect all products in customer cart

```json
GET /cart/<customer_id>
```

* Add Cart, add product into customer cart

```json
POST /cart/add
{
  "customer_id": 1,
  "product_id": 1,
  "quantity": 1
}
```

* Remove Product Cart, remove product in customer cart

```json
POST /cart/remove
{
  "customer_id": 1,
  "product_id": 1
}
```

### Order

* Add Order, order all product in cart

```json
POST /order/add
{
  "customer_id": 1
}
```

* Get Total Product Order, get total product quantity ordered

```json
GET /order/product/<product_id>
```

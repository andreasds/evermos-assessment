-- create database online_store
CREATE DATABASE IF NOT EXISTS online_store;

USE online_store;

-- create customers
CREATE TABLE IF NOT EXISTS customers (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE
);

-- create products
CREATE TABLE IF NOT EXISTS products (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    product_name VARCHAR(100) NOT NULL,
    stock INT NOT NULL DEFAULT 0
);

-- create new_stocks
-- log stock added
CREATE TABLE IF NOT EXISTS new_stocks (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    product_id INT NOT NULL,
    stock INT NOT NULL,
    added_date TIMESTAMP NOT NULL,
    CONSTRAINT fk_stock_product FOREIGN KEY (product_id) REFERENCES products(id)
);

-- create carts
CREATE TABLE IF NOT EXISTS carts (
    customer_id INT NOT NULL,
    product_id INT NOT NULL,
    quantity INT NOT NULL,
    CONSTRAINT fk_cart_customer FOREIGN KEY (customer_id) REFERENCES customers(id),
    CONSTRAINT fk_cart_product FOREIGN KEY (product_id) REFERENCES products(id),
    PRIMARY KEY (customer_id, product_id)
);

-- create orders
CREATE TABLE IF NOT EXISTS orders (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    order_number VARCHAR(20) NOT NULL,
    customer_id INT NOT NULL,
    issued_date TIMESTAMP NOT NULL,
    order_status TINYINT NOT NULL DEFAULT 1, -- 0 = PAID, 1 = WAITING, 2 = CANCELLED
    CONSTRAINT fk_order_customer FOREIGN KEY (customer_id) REFERENCES customers(id)
);

-- create order_products
-- list of product in one order number
CREATE TABLE IF NOT EXISTS order_products (
    order_id INT NOT NULL,
    product_id INT NOT NULL,
    quantity INT NOT NULL,
    CONSTRAINT fk_order_product_order FOREIGN KEY (order_id) REFERENCES orders(id),
    CONSTRAINT fk_order_product_product FOREIGN KEY (product_id) REFERENCES products(id),
    PRIMARY KEY (order_id, product_id)
);

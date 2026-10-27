CREATE DATABASE IF NOT EXISTS dashboard_vendas CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE dashboard_vendas;

CREATE TABLE IF NOT EXISTS sales (
 id BIGINT AUTO_INCREMENT PRIMARY KEY,
 order_date DATE NOT NULL,
 order_id VARCHAR(30) NOT NULL UNIQUE,
 product VARCHAR(100) NOT NULL,
 category VARCHAR(60) NOT NULL,
 state CHAR(2) NOT NULL,
 quantity INT NOT NULL CHECK (quantity > 0),
 unit_price DECIMAL(12,2) NOT NULL CHECK (unit_price >= 0),
 unit_cost DECIMAL(12,2) NOT NULL CHECK (unit_cost >= 0),
 INDEX idx_sales_date (order_date),
 INDEX idx_sales_category (category)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

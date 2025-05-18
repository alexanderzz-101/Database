-- 1. Create the database and use it
CREATE DATABASE IF NOT EXISTS `CCCS105`;
USE `CCCS105`;

-- 2. Create tables
CREATE TABLE `Vendors` (
    `vendor_id` INT AUTO_INCREMENT PRIMARY KEY, 
    `name` VARCHAR(100) NOT NULL,
    `contact_info` TEXT,
    `stall_number` VARCHAR(20)
);

CREATE TABLE `Products` (
    `product_id` INT AUTO_INCREMENT PRIMARY KEY,
    `vendor_id` INT NOT NULL,
    `name` VARCHAR(100) NOT NULL,
    `category` VARCHAR(50),
    `unit` VARCHAR(20),
    FOREIGN KEY (vendor_id) REFERENCES Vendors(vendor_id) ON DELETE CASCADE
);

CREATE TABLE `Inventory_Stock` (
    `inventory_id` INT AUTO_INCREMENT PRIMARY KEY,
    `product_id` INT NOT NULL,
    `quantity_available` DECIMAL(10, 2) NOT NULL,
    `date_recorded` DATE NOT NULL,
    FOREIGN KEY (product_id) REFERENCES Products(product_id) ON DELETE CASCADE
);

CREATE TABLE `Orders` (
    `order_id` INT AUTO_INCREMENT PRIMARY KEY,
    `vendor_id` INT NOT NULL,
    `order_date` DATE NOT NULL,
    `total_amount` DECIMAL(10, 2),
    FOREIGN KEY (vendor_id) REFERENCES Vendors(vendor_id) ON DELETE CASCADE
);

CREATE TABLE `Order_Items` (
    `order_item_id` INT AUTO_INCREMENT PRIMARY KEY,
    `order_id` INT NOT NULL,
    `product_id` INT NOT NULL,
    `quantity_sold` DECIMAL(10, 2) NOT NULL,
    `unit_price` DECIMAL(10, 2) NOT NULL,
    FOREIGN KEY (order_id) REFERENCES Orders(order_id) ON DELETE CASCADE,
    FOREIGN KEY (product_id) REFERENCES Products(product_id) ON DELETE CASCADE
);

INSERT INTO `Vendors` (`name`, `contact_info`, `stall_number`)
VALUES 
('Masitasan ni Kuya Rence', 'kuyarence@example.com', 'Stall 2'),
('Apple ni Macmac', 'etomac@example.com', 'Stall 1'),
('Gulayan ni Pay Juswa', 'jarico@example.com', 'Stall 3'),
('Sariwang Bunga ni Bayn', 'thebayn@example.com', 'Stall 4'),
('Blessie Meatshop', 'blisipeyt@example.com', 'Stall 10'),
('Bakalan Gin ni JJ', 'jaegerdabest@example.com', 'Stall 12'),
('Prutas ni Carlo', 'elonnas@example.com', 'Stall 6'),
('Sariwang Isdang Buhi ni Renzzo', 'damafia@example.com', 'Stall 5');

INSERT INTO `Products` (`vendor_id`, `name`, `category`, `unit`)
VALUES
(1, 'Tomatoes', 'Vegetable', 'kg'),
(1, 'Cucumbers', 'Vegetable', 'kg'),
(2, 'Apples', 'Fruit', 'kg'),
(2, 'Bananas', 'Fruit', 'kg'),
(3, 'Spinach', 'Vegetable', 'kg'),
(3, 'Lettuce', 'Vegetable', 'kg'),
(4, 'Carrots', 'Vegetable', 'kg'),
(4, 'Bell Peppers', 'Vegetable', 'kg'),
(5, 'Pork Chops', 'Meat', 'kg'),
(5, 'Pork Belly', 'Meat', 'kg'),
(5, 'Chicken Breast', 'Meat', 'kg'),
(5, 'Beef Steak', 'Meat', 'kg'),
(5, 'Ground Beef', 'Meat', 'kg'),
(6, 'Gin', 'Beverage', 'L'),
(6, 'Red Horse', 'Beverage', 'L'),
(7, 'Oranges', 'Fruit', 'kg'),
(7, 'Grapes', 'Fruit', 'kg'),
(7, 'Mangoes', 'Fruit', 'kg'),
(7, 'Pineapples', 'Fruit', 'kg'),
(8, 'Tilapia', 'Fish', 'kg'),
(8, 'Catfish', 'Fish', 'kg');

INSERT INTO `Inventory_Stock` (`product_id`, `quantity_available`, `date_recorded`)
VALUES
(1, 78, '2025-05-18'),
(2, 26, '2025-05-18'),
(3, 92, '2025-05-18'),
(4, 47, '2025-05-18'),
(5, 31, '2025-05-18'),
(6, 64, '2025-05-18'),
(7, 15, '2025-05-18'),
(8, 120, '2025-05-18'),
(9, 100, '2025-05-18'),
(10, 88, '2025-05-18'),
(11, 55, '2025-05-18'),
(12, 72, '2025-05-18'),
(13, 43, '2025-05-18'),
(14, 19, '2025-05-18'),
(15, 12, '2025-05-18'),
(16, 50, '2025-05-18'),
(17, 44, '2025-05-18'),
(18, 67, '2025-05-18'),
(19, 39, '2025-05-18'),
(20, 96, '2025-05-18'),
(21, 84, '2025-05-18');
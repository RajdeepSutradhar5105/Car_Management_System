-- Use the database
USE car_management_system;

-- Drop existing tables in the correct order to avoid foreign key errors
DROP TABLE IF EXISTS transactions;
DROP TABLE IF EXISTS cars;
DROP TABLE IF EXISTS users; -- This is the old single user table

-- Create a table for managers
CREATE TABLE managers (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(255) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL
);

-- Create a table for sellers
CREATE TABLE sellers (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(255) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL
);

-- Create a table for buyers
CREATE TABLE buyers (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(255) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL
);

-- Re-create the cars table, linking to the new 'sellers' table
CREATE TABLE cars (
    id INT AUTO_INCREMENT PRIMARY KEY,
    make VARCHAR(255) NOT NULL,
    model VARCHAR(255) NOT NULL,
    year INT NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    status ENUM('available', 'sold') NOT NULL DEFAULT 'available',
    seller_id INT,
    FOREIGN KEY (seller_id) REFERENCES sellers(id) ON DELETE SET NULL
);

-- Re-create the transactions table, linking to the new 'buyers' and 'sellers' tables
CREATE TABLE transactions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    car_id INT,
    buyer_id INT,
    seller_id INT,
    sale_price DECIMAL(10, 2) NOT NULL,
    transaction_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (car_id) REFERENCES cars(id),
    FOREIGN KEY (buyer_id) REFERENCES buyers(id) ON DELETE SET NULL,
    FOREIGN KEY (seller_id) REFERENCES sellers(id) ON DELETE SET NULL
);

-- Insert a manager
INSERT INTO managers (username, password) VALUES ('manager1', 'managerpass');

-- Insert a seller
INSERT INTO sellers (username, password) VALUES ('seller1', 'sellerpass');

-- Insert a buyer
INSERT INTO buyers (username, password) VALUES ('buyer1', 'buyerpass');

-- Insert some cars for sale by the new seller (whose ID is 1)
INSERT INTO cars (make, model, year, price, seller_id) VALUES
('Toyota', 'Camry', 2021, 25000.00, 1),
('Honda', 'Civic', 2022, 23000.00, 1),
('Ford', 'Mustang', 2020, 35000.00, 1);

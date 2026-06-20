-- Create database 
CREATE DATABASE IF NOT EXISTS labo05_payments_db;
USE labo05_payments_db;

-- Payments table
DROP TABLE IF EXISTS payments;
CREATE TABLE payments (
    id INT AUTO_INCREMENT PRIMARY KEY,
    order_id INT NOT NULL,
    user_id INT NOT NULL,
    total_amount DECIMAL(12,2) NOT NULL,
    is_paid BOOLEAN NOT NULL DEFAULT false,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Mock data: payments
INSERT INTO payments (order_id, user_id, total_amount, is_paid) VALUES
(1, 1, 1999.99, false),
(2, 2, 59.50, false);


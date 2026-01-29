CREATE DATABASE traffic_db;
USE traffic_db;

CREATE TABLE vehicle_owners (
    vehicle_number VARCHAR(20) PRIMARY KEY,
    owner_name VARCHAR(100),
    email VARCHAR(100),
    phone VARCHAR(15)
);

INSERT INTO vehicle_owners VALUES
('MH04FA7451', 'Hariom Dixit', 'hariomdixit2002@gmail.com', '9876543210'),
('MH12AB1234', 'Amit Patil', 'amit@gmail.com', '9123456789'),
('MH01CD5678', 'Neha Joshi', 'neha@gmail.com', '9988776655');

CREATE TABLE traffic_fines (
    id INT AUTO_INCREMENT PRIMARY KEY,
    vehicle_number VARCHAR(20),
    email VARCHAR(100),
    fine INT,
    paid CHAR(1)
);

INSERT INTO vehicle_owners VALUES
('HR26FC2782', 'Harry Potter', 'hariomdixit2002@gmail.com', '9876543210');

select * from vehicle_owners;

select * from traffic_fines;

ALTER TABLE traffic_fines
ADD COLUMN violation_type VARCHAR(50);

CREATE TABLE violation_types (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50),
    fine INT
);

INSERT INTO violation_types (name, fine) VALUES
('No Helmet', 500),
('Signal Jump', 1000),
('Over Speeding', 1500),
('Wrong Parking', 300);




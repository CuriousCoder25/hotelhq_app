-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Jun 08, 2025 at 10:50 AM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `hotel_management`
--

-- --------------------------------------------------------

--
-- Table structure for table `billing`
--

CREATE TABLE `billing` (
  `Bill_no` int(11) NOT NULL,
  `User_ID` int(11) NOT NULL,
  `Item` varchar(255) NOT NULL,
  `Quantity` int(11) DEFAULT 1,
  `Rate` decimal(10,2) NOT NULL,
  `Total_Tax` decimal(10,2) DEFAULT 0.00,
  `Total_amount` decimal(10,2) NOT NULL,
  `Billed_by` varchar(100) DEFAULT NULL,
  `Discount` decimal(10,2) DEFAULT 0.00,
  `Date_Time` timestamp NOT NULL DEFAULT current_timestamp(),
  `Status` enum('Pending','Paid','Cancelled','Refunded') DEFAULT 'Pending',
  `payment_method` enum('Cash','Card','Online','Bank Transfer') DEFAULT NULL,
  `notes` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `billing`
--

INSERT INTO `billing` (`Bill_no`, `User_ID`, `Item`, `Quantity`, `Rate`, `Total_Tax`, `Total_amount`, `Billed_by`, `Discount`, `Date_Time`, `Status`, `payment_method`, `notes`) VALUES
(1, 1, 'Room Charge - Standard', 3, 100.00, 30.00, 330.00, 'reception01', 0.00, '2025-05-31 15:24:31', 'Paid', 'Card', NULL),
(2, 1, 'Restaurant Service', 1, 45.00, 4.50, 49.50, 'reception01', 0.00, '2025-05-31 15:24:31', 'Paid', 'Card', NULL),
(3, 2, 'Room Charge - Deluxe', 2, 150.00, 30.00, 330.00, 'reception01', 0.00, '2025-05-31 15:24:31', 'Pending', NULL, NULL),
(4, 3, 'Laundry Service', 1, 25.00, 2.50, 27.50, 'reception01', 0.00, '2025-05-31 15:24:31', 'Paid', 'Cash', NULL);

-- --------------------------------------------------------

--
-- Table structure for table `customer`
--

CREATE TABLE `customer` (
  `User_ID` int(11) NOT NULL,
  `Legal_Docs` varchar(100) DEFAULT NULL,
  `Room_ID` int(11) DEFAULT NULL,
  `Bill_no` int(11) DEFAULT NULL,
  `First_Name` varchar(100) NOT NULL,
  `Last_Name` varchar(100) NOT NULL,
  `Mobile_no` varchar(20) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  `address` text DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `updated_at` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `customer`
--

INSERT INTO `customer` (`User_ID`, `Legal_Docs`, `Room_ID`, `Bill_no`, `First_Name`, `Last_Name`, `Mobile_no`, `email`, `address`, `created_at`, `updated_at`) VALUES
(1, 'CIT001', 4, 1, 'John', 'Doe', '+1234567890', 'john.doe@email.com', '123 Main St, City, Country', '2025-05-31 15:24:31', '2025-05-31 15:24:31'),
(2, 'PASS001', 2, 3, 'Jane', 'Smith', '+0987654321', 'jane.smith@email.com', '456 Oak Ave, City, Country', '2025-05-31 15:24:31', '2025-05-31 15:24:31'),
(3, 'CIT002', 1, 4, 'Bob', 'Johnson', '+1122334455', 'bob.johnson@email.com', '789 Pine Rd, City, Country', '2025-05-31 15:24:31', '2025-05-31 15:24:31');

-- --------------------------------------------------------

--
-- Table structure for table `legal_docs`
--

CREATE TABLE `legal_docs` (
  `Ldoc_ID` int(11) NOT NULL,
  `User_ID` int(11) NOT NULL,
  `Citizenship_Photo` varchar(255) DEFAULT NULL,
  `Passport_Photo` varchar(255) DEFAULT NULL,
  `document_type` enum('Citizenship','Passport','License','Other') NOT NULL,
  `document_number` varchar(50) DEFAULT NULL,
  `expiry_date` date DEFAULT NULL,
  `verified` tinyint(1) DEFAULT 0,
  `uploaded_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `verified_at` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `legal_docs`
--

INSERT INTO `legal_docs` (`Ldoc_ID`, `User_ID`, `Citizenship_Photo`, `Passport_Photo`, `document_type`, `document_number`, `expiry_date`, `verified`, `uploaded_at`, `verified_at`) VALUES
(1, 1, 'john_doe_citizenship.jpg', NULL, 'Citizenship', 'CIT123456789', '2030-12-31', 1, '2025-05-31 15:24:31', NULL),
(2, 2, 'jane_smith_passport.jpg', NULL, 'Passport', 'PASS987654321', '2028-06-15', 1, '2025-05-31 15:24:31', NULL),
(3, 3, 'bob_johnson_citizenship.jpg', NULL, 'Citizenship', 'CIT456789123', '2029-03-20', 0, '2025-05-31 15:24:31', NULL);

-- --------------------------------------------------------

--
-- Table structure for table `login`
--

CREATE TABLE `login` (
  `Username` varchar(50) NOT NULL,
  `User_ID` int(11) NOT NULL,
  `Role_ID` int(11) NOT NULL,
  `Password` varchar(255) NOT NULL,
  `last_login` timestamp NULL DEFAULT NULL,
  `is_active` tinyint(1) DEFAULT 1,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `updated_at` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `login`
--

INSERT INTO `login` (`Username`, `User_ID`, `Role_ID`, `Password`, `last_login`, `is_active`, `created_at`, `updated_at`) VALUES
('admin', 1, 1, '$2y$10$92IXUNpkjO0rOQ5byMi.Ye4oKoEa3Ro9llC/.og/at2.uheWG/igi', NULL, 1, '2025-05-31 15:24:31', '2025-05-31 15:24:31'),
('manager01', 2, 2, '$2y$10$92IXUNpkjO0rOQ5byMi.Ye4oKoEa3Ro9llC/.og/at2.uheWG/igi', NULL, 1, '2025-05-31 15:24:31', '2025-05-31 15:24:31'),
('reception01', 3, 3, '$2y$10$92IXUNpkjO0rOQ5byMi.Ye4oKoEa3Ro9llC/.og/at2.uheWG/igi', NULL, 1, '2025-05-31 15:24:31', '2025-05-31 15:24:31');

-- --------------------------------------------------------

--
-- Table structure for table `role`
--

CREATE TABLE `role` (
  `Role_ID` int(11) NOT NULL,
  `Username` varchar(50) NOT NULL,
  `Role_name` varchar(100) NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `updated_at` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `role`
--

INSERT INTO `role` (`Role_ID`, `Username`, `Role_name`, `created_at`, `updated_at`) VALUES
(1, 'admin', 'Administrator', '2025-05-31 15:24:31', '2025-05-31 15:24:31'),
(2, 'manager', 'Hotel Manager', '2025-05-31 15:24:31', '2025-05-31 15:24:31'),
(3, 'receptionist', 'Front Desk Receptionist', '2025-05-31 15:24:31', '2025-05-31 15:24:31'),
(4, 'housekeeping', 'Housekeeping Staff', '2025-05-31 15:24:31', '2025-05-31 15:24:31'),
(5, 'customer', 'Hotel Guest', '2025-05-31 15:24:31', '2025-05-31 15:24:31');

-- --------------------------------------------------------

--
-- Table structure for table `room`
--

CREATE TABLE `room` (
  `Room_ID` int(11) NOT NULL,
  `Status_ID` int(11) NOT NULL,
  `User_ID` int(11) DEFAULT NULL,
  `Room_Category` varchar(50) NOT NULL,
  `Room_Price` decimal(10,2) NOT NULL,
  `Status` enum('Available','Occupied','Maintenance','Reserved') DEFAULT 'Available',
  `Booking_Date_Time` timestamp NULL DEFAULT NULL,
  `Check_In` timestamp NULL DEFAULT NULL,
  `Check_Out` timestamp NULL DEFAULT NULL,
  `room_number` varchar(10) NOT NULL,
  `floor_number` int(11) DEFAULT NULL,
  `max_occupancy` int(11) DEFAULT 2,
  `amenities` text DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `updated_at` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `room`
--

INSERT INTO `room` (`Room_ID`, `Status_ID`, `User_ID`, `Room_Category`, `Room_Price`, `Status`, `Booking_Date_Time`, `Check_In`, `Check_Out`, `room_number`, `floor_number`, `max_occupancy`, `amenities`, `created_at`, `updated_at`) VALUES
(1, 1, NULL, 'Standard', 100.00, 'Available', NULL, NULL, NULL, '101', 1, 2, 'AC, TV, WiFi, Private Bathroom', '2025-05-31 15:24:31', '2025-05-31 15:24:31'),
(2, 2, 2, 'Deluxe', 150.00, 'Available', NULL, NULL, NULL, '201', 2, 2, 'AC, TV, WiFi, Private Bathroom, Mini Bar', '2025-05-31 15:24:31', '2025-05-31 15:24:31'),
(3, 3, NULL, 'Suite', 250.00, 'Available', NULL, NULL, NULL, '301', 3, 4, 'AC, TV, WiFi, Private Bathroom, Mini Bar, Living Room', '2025-05-31 15:24:31', '2025-05-31 15:24:31'),
(4, 4, 1, 'Standard', 100.00, 'Occupied', NULL, NULL, NULL, '102', 1, 2, 'AC, TV, WiFi, Private Bathroom', '2025-05-31 15:24:31', '2025-05-31 15:24:31'),
(5, 5, NULL, 'Deluxe', 150.00, 'Maintenance', NULL, NULL, NULL, '202', 2, 2, 'AC, TV, WiFi, Private Bathroom, Mini Bar', '2025-05-31 15:24:31', '2025-05-31 15:24:31');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `billing`
--
ALTER TABLE `billing`
  ADD PRIMARY KEY (`Bill_no`),
  ADD KEY `User_ID` (`User_ID`),
  ADD KEY `idx_billing_status` (`Status`),
  ADD KEY `idx_billing_date` (`Date_Time`);

--
-- Indexes for table `customer`
--
ALTER TABLE `customer`
  ADD PRIMARY KEY (`User_ID`),
  ADD KEY `fk_customer_room` (`Room_ID`),
  ADD KEY `fk_customer_bill` (`Bill_no`),
  ADD KEY `idx_customer_mobile` (`Mobile_no`),
  ADD KEY `idx_customer_email` (`email`);

--
-- Indexes for table `legal_docs`
--
ALTER TABLE `legal_docs`
  ADD PRIMARY KEY (`Ldoc_ID`),
  ADD KEY `User_ID` (`User_ID`),
  ADD KEY `idx_legal_docs_type` (`document_type`),
  ADD KEY `idx_legal_docs_verified` (`verified`);

--
-- Indexes for table `login`
--
ALTER TABLE `login`
  ADD PRIMARY KEY (`Username`),
  ADD UNIQUE KEY `User_ID` (`User_ID`),
  ADD KEY `Role_ID` (`Role_ID`),
  ADD KEY `idx_login_user_id` (`User_ID`);

--
-- Indexes for table `role`
--
ALTER TABLE `role`
  ADD PRIMARY KEY (`Role_ID`);

--
-- Indexes for table `room`
--
ALTER TABLE `room`
  ADD PRIMARY KEY (`Room_ID`),
  ADD UNIQUE KEY `room_number` (`room_number`),
  ADD KEY `User_ID` (`User_ID`),
  ADD KEY `idx_room_status` (`Status`),
  ADD KEY `idx_room_category` (`Room_Category`),
  ADD KEY `idx_room_number` (`room_number`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `billing`
--
ALTER TABLE `billing`
  MODIFY `Bill_no` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT for table `customer`
--
ALTER TABLE `customer`
  MODIFY `User_ID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `legal_docs`
--
ALTER TABLE `legal_docs`
  MODIFY `Ldoc_ID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `role`
--
ALTER TABLE `role`
  MODIFY `Role_ID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT for table `room`
--
ALTER TABLE `room`
  MODIFY `Room_ID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `billing`
--
ALTER TABLE `billing`
  ADD CONSTRAINT `billing_ibfk_1` FOREIGN KEY (`User_ID`) REFERENCES `customer` (`User_ID`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `customer`
--
ALTER TABLE `customer`
  ADD CONSTRAINT `fk_customer_bill` FOREIGN KEY (`Bill_no`) REFERENCES `billing` (`Bill_no`) ON DELETE SET NULL ON UPDATE CASCADE,
  ADD CONSTRAINT `fk_customer_room` FOREIGN KEY (`Room_ID`) REFERENCES `room` (`Room_ID`) ON DELETE SET NULL ON UPDATE CASCADE;

--
-- Constraints for table `legal_docs`
--
ALTER TABLE `legal_docs`
  ADD CONSTRAINT `legal_docs_ibfk_1` FOREIGN KEY (`User_ID`) REFERENCES `customer` (`User_ID`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `login`
--
ALTER TABLE `login`
  ADD CONSTRAINT `login_ibfk_1` FOREIGN KEY (`Role_ID`) REFERENCES `role` (`Role_ID`) ON UPDATE CASCADE;

--
-- Constraints for table `room`
--
ALTER TABLE `room`
  ADD CONSTRAINT `room_ibfk_1` FOREIGN KEY (`User_ID`) REFERENCES `customer` (`User_ID`) ON DELETE SET NULL ON UPDATE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;

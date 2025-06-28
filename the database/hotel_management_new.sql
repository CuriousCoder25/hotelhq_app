-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Jun 26, 2025 at 11:58 AM
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
  `User_ID` int(11) DEFAULT NULL,
  `Item` varchar(100) DEFAULT NULL,
  `Quantity` int(11) DEFAULT NULL,
  `Rate` decimal(10,2) DEFAULT NULL,
  `Total_Tax` decimal(10,2) DEFAULT NULL,
  `Total_amount` decimal(10,2) DEFAULT NULL,
  `Billed_by` varchar(50) DEFAULT NULL,
  `Status` enum('Pending','Paid') DEFAULT 'Pending',
  `payment_method` varchar(20) DEFAULT NULL,
  `Date_Time` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `customer`
--

CREATE TABLE `customer` (
  `User_ID` int(11) NOT NULL,
  `First_Name` varchar(50) NOT NULL,
  `Last_Name` varchar(50) NOT NULL,
  `Mobile_no` varchar(15) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  `address` text DEFAULT NULL,
  `Room_ID` int(11) DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `document_status` enum('Pending','Approved','Rejected') DEFAULT 'Pending',
  `verification_notes` text DEFAULT NULL COMMENT 'Staff notes for document verification',
  `verified_by` varchar(100) DEFAULT NULL COMMENT 'Username of staff who verified documents',
  `verification_date` datetime DEFAULT NULL COMMENT 'Date when documents were verified'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `customer`
--

INSERT INTO `customer` (`User_ID`, `First_Name`, `Last_Name`, `Mobile_no`, `email`, `address`, `Room_ID`, `created_at`, `document_status`, `verification_notes`, `verified_by`, `verification_date`) VALUES
(6, 'ram', 'singht', '949u508308508', 'gauhrgushr@gmail.com', NULL, NULL, '2025-06-10 05:06:30', 'Rejected', 'Please post a more clear picture', 'suresh012', '2025-06-10 23:02:12'),
(8, 'Gaurav', 'Kathayat', '9865622145', 'gauravkathayat@nast.edu.np', NULL, NULL, '2025-06-10 05:53:28', 'Rejected', 'd', 'suresh012', '2025-06-10 22:53:15');

-- --------------------------------------------------------

--
-- Table structure for table `login`
--

CREATE TABLE `login` (
  `User_ID` int(11) NOT NULL,
  `Username` varchar(50) NOT NULL,
  `Password` varchar(255) NOT NULL,
  `Role_ID` int(11) DEFAULT NULL,
  `is_active` tinyint(1) DEFAULT 1,
  `last_login` datetime DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `login`
--

INSERT INTO `login` (`User_ID`, `Username`, `Password`, `Role_ID`, `is_active`, `last_login`, `created_at`) VALUES
(6, 'ram', 'scrypt:32768:8:1$D9eM9LbGCB7mUdHt$054703e39ba27fafc5504cb9cd83fc113ec0229c0a8e0ad0a67e537561026969d461d56063a15eb778f1e2cd9901a3d936a5a41be2c020bdcc4a0bcdb575137b', 3, 1, '2025-06-10 10:55:20', '2025-06-10 09:11:01'),
(7, 'admin', 'scrypt:32768:8:1$ktGSbCFQZutDMNXG$dc8a8dcd23b475446dde0320ae3df062cd8f80ab13de70869cacac4500b224d3468ecafe57c09ff5889e6e79088ffc30235fb4d5a0944a62bdb458075fc0b32c', 1, 1, '2025-06-26 15:22:01', '2025-06-10 09:11:01'),
(8, 'gaurav01', 'scrypt:32768:8:1$bk8rbKo5A2QriBqQ$106f3656d268087f59723ce8c82ee861bc79f4e78128869ef57749db9973c85f1eccbc3b3ac5222d8ac7f0cb54423583e3007e98b003dcd03721611b961aabe7', 3, 1, '2025-06-26 15:24:31', '2025-06-10 09:11:01'),
(9, 'staff01', 'scrypt:32768:8:1$sWQvl6WqXBPePssT$b412d6f02baaf74914d53c80b21fd4579fa73a6ca5842cacc8d415b95d260e99a4c59cde55d510944e083f69fb42068937df88821ca3f5467b33936638612a3a', 2, 1, NULL, '2025-06-10 09:18:59'),
(10, 'suresh012', 'scrypt:32768:8:1$8YQwgQYqHUUULwsm$321819381ca1b70be170d2c83c6db92514d03dac27c93d3f9f82fadf25c988f6aea7192cd6c6a7b362d7c76655218351e75edbc0f44957111a31a2e33eb92f92', 2, 1, '2025-06-26 15:23:33', '2025-06-10 09:31:44');

-- --------------------------------------------------------

--
-- Table structure for table `role`
--

CREATE TABLE `role` (
  `Role_ID` int(11) NOT NULL,
  `Role_name` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `role`
--

INSERT INTO `role` (`Role_ID`, `Role_name`) VALUES
(1, 'Admin'),
(2, 'Staff'),
(3, 'Customer');

-- --------------------------------------------------------

--
-- Table structure for table `room`
--

CREATE TABLE `room` (
  `Room_ID` int(11) NOT NULL,
  `room_number` varchar(10) NOT NULL,
  `Status` enum('Available','Occupied','Maintenance') DEFAULT 'Available',
  `Room_Price` decimal(10,2) NOT NULL DEFAULT 0.00,
  `User_ID` int(11) DEFAULT NULL,
  `Check_In` datetime DEFAULT NULL,
  `Check_Out` datetime DEFAULT NULL,
  `Room_type` varchar(50) DEFAULT 'Standard',
  `description` text DEFAULT NULL,
  `room_image` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `room`
--

INSERT INTO `room` (`Room_ID`, `room_number`, `Status`, `Room_Price`, `User_ID`, `Check_In`, `Check_Out`, `Room_type`, `description`, `room_image`) VALUES
(1, '101', 'Occupied', 0.00, 8, '2025-06-10 12:12:40', NULL, 'Single', '', '26ba023a-d73d-4240-98cd-fb8805813546_2.jpg'),
(2, '102', 'Occupied', 0.00, 8, '2025-06-26 15:25:25', NULL, 'Standard', NULL, NULL),
(3, '103', 'Available', 0.00, NULL, NULL, NULL, 'Standard', NULL, NULL),
(4, '201', 'Available', 0.00, NULL, NULL, NULL, 'Standard', NULL, NULL),
(5, '202', 'Available', 0.00, NULL, NULL, NULL, 'Standard', NULL, NULL),
(6, '203', 'Available', 0.00, NULL, NULL, NULL, 'Standard', NULL, NULL),
(7, '301', 'Available', 0.00, NULL, NULL, NULL, 'Standard', NULL, NULL),
(8, '302', 'Available', 0.00, NULL, NULL, NULL, 'Standard', NULL, NULL),
(10, '107', 'Available', 1001.14, NULL, NULL, NULL, 'Single', 'very good', 'fa0fec83-8935-4391-b2f4-207b704e12e3_download (10).jpeg');

-- --------------------------------------------------------

--
-- Table structure for table `staff`
--

CREATE TABLE `staff` (
  `User_ID` int(11) NOT NULL,
  `First_Name` varchar(50) NOT NULL,
  `Last_Name` varchar(50) NOT NULL,
  `email` varchar(100) DEFAULT NULL,
  `Mobile_no` varchar(15) DEFAULT NULL,
  `position` varchar(50) DEFAULT NULL,
  `hire_date` date DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `staff`
--

INSERT INTO `staff` (`User_ID`, `First_Name`, `Last_Name`, `email`, `Mobile_no`, `position`, `hire_date`, `created_at`) VALUES
(9, 'John', 'Doe', 'john.doe@hotel.com', '1234567890', 'Front Desk', '2025-06-10', '2025-06-10 09:18:59'),
(10, 'Suresh', 'Joshi', 'suresh@gmail.com', '9865622445', 'Manager', '2025-06-10', '2025-06-10 09:31:44');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `billing`
--
ALTER TABLE `billing`
  ADD PRIMARY KEY (`Bill_no`),
  ADD KEY `User_ID` (`User_ID`);

--
-- Indexes for table `customer`
--
ALTER TABLE `customer`
  ADD PRIMARY KEY (`User_ID`),
  ADD KEY `Room_ID` (`Room_ID`);

--
-- Indexes for table `login`
--
ALTER TABLE `login`
  ADD PRIMARY KEY (`User_ID`),
  ADD UNIQUE KEY `Username` (`Username`),
  ADD KEY `Role_ID` (`Role_ID`);

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
  ADD UNIQUE KEY `room_number` (`room_number`);

--
-- Indexes for table `staff`
--
ALTER TABLE `staff`
  ADD PRIMARY KEY (`User_ID`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `billing`
--
ALTER TABLE `billing`
  MODIFY `Bill_no` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `customer`
--
ALTER TABLE `customer`
  MODIFY `User_ID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;

--
-- AUTO_INCREMENT for table `login`
--
ALTER TABLE `login`
  MODIFY `User_ID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- AUTO_INCREMENT for table `role`
--
ALTER TABLE `role`
  MODIFY `Role_ID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `room`
--
ALTER TABLE `room`
  MODIFY `Room_ID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `billing`
--
ALTER TABLE `billing`
  ADD CONSTRAINT `billing_ibfk_1` FOREIGN KEY (`User_ID`) REFERENCES `customer` (`User_ID`);

--
-- Constraints for table `customer`
--
ALTER TABLE `customer`
  ADD CONSTRAINT `customer_ibfk_1` FOREIGN KEY (`Room_ID`) REFERENCES `room` (`Room_ID`);

--
-- Constraints for table `login`
--
ALTER TABLE `login`
  ADD CONSTRAINT `login_ibfk_1` FOREIGN KEY (`Role_ID`) REFERENCES `role` (`Role_ID`);

--
-- Constraints for table `staff`
--
ALTER TABLE `staff`
  ADD CONSTRAINT `staff_ibfk_1` FOREIGN KEY (`User_ID`) REFERENCES `login` (`User_ID`) ON DELETE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;

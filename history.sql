-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Nov 27, 2024 at 02:29 PM
-- Server version: 10.4.28-MariaDB
-- PHP Version: 8.2.4

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `history`
--

-- --------------------------------------------------------

--
-- Table structure for table `history`
--

CREATE TABLE `history` (
  `id` int(11) NOT NULL,
  `filename` varchar(100) NOT NULL,
  `predictions_skin_conditions` varchar(200) NOT NULL,
  `predictions_skin_type` varchar(200) NOT NULL,
  `timestamp` datetime NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `history`
--

INSERT INTO `history` (`id`, `filename`, `predictions_skin_conditions`, `predictions_skin_type`, `timestamp`) VALUES
(4, 'e98ef592-7459-4b1c-b2dc-29bd2e69ef77.jpg', 'Acne: 0.98, Eye Bags: 0.03', 'Oily: 0.65, Normal: 0.05, Dry: 0.30', '2024-11-26 09:22:18'),
(5, '0f289743-3ccc-4232-940c-47c36ca244d0.jpg', 'Acne: 0.88, Eye Bags: 0.34', 'Oily: 0.00, Normal: 0.00, Dry: 1.00', '2024-11-26 09:22:40'),
(6, '2a37e209-4e04-4af2-817e-478e93650fc7.jpg', 'Acne: 0.41, Eye Bags: 0.88', 'Oily: 0.00, Normal: 0.00, Dry: 1.00', '2024-11-26 09:22:58'),
(7, 'bf63c1b2-10c2-4baa-8e5e-cefa524f12a4.jpg', 'Acne: 0.88, Eye Bags: 0.34', 'Oily: 0.00, Normal: 0.00, Dry: 1.00', '2024-11-27 08:26:48'),
(8, '5d838ce4-1f30-4040-90ef-9d63a0ae554d.jpg', 'Acne: 0.22, Eye Bags: 0.86', 'Oily: 0.22, Normal: 0.77, Dry: 0.01', '2024-11-27 13:13:21'),
(9, 'd5120ae8-bb81-4ac9-9cd8-b61f1d5eaada.jpg', 'Acne: 0.22, Eye Bags: 0.86', 'Oily: 0.22, Normal: 0.77, Dry: 0.01', '2024-11-27 13:13:36');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `history`
--
ALTER TABLE `history`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `history`
--
ALTER TABLE `history`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=10;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;

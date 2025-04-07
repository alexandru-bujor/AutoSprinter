-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Gazdă: 127.0.0.1
-- Timp de generare: mart. 27, 2025 la 10:33 AM
-- Versiune server: 10.4.32-MariaDB
-- Versiune PHP: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Bază de date: `autosprinter`
--

-- --------------------------------------------------------

--
-- Structură tabel pentru tabel `cars`
--

CREATE TABLE `cars` (
  `id` int(11) NOT NULL,
  `slug` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `model` varchar(255) NOT NULL,
  `year` int(11) NOT NULL,
  `registration` varchar(255) DEFAULT NULL,
  `fuel` varchar(100) DEFAULT NULL,
  `transmission` varchar(100) DEFAULT NULL,
  `body_type` varchar(100) DEFAULT NULL,
  `transport_type` varchar(100) DEFAULT NULL,
  `color` varchar(100) DEFAULT NULL,
  `engine_capacity` varchar(50) DEFAULT NULL,
  `seats` int(11) DEFAULT NULL,
  `mileage` varchar(50) DEFAULT NULL,
  `drive_type` varchar(100) DEFAULT NULL,
  `price` varchar(50) DEFAULT NULL,
  `monthly_rate` varchar(50) DEFAULT NULL,
  `contact_phone` varchar(50) DEFAULT NULL,
  `image` varchar(512) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Eliminarea datelor din tabel `cars`
--

INSERT INTO `cars` (`id`, `slug`, `name`, `model`, `year`, `registration`, `fuel`, `transmission`, `body_type`, `transport_type`, `color`, `engine_capacity`, `seats`, `mileage`, `drive_type`, `price`, `monthly_rate`, `contact_phone`, `image`) VALUES
(1, '81736935', '', 'Mercedes Sprinter', 2016, NULL, 'Diesel', 'Manual', NULL, NULL, 'Albastru', '2987', NULL, '198238', NULL, '25750', NULL, '069191783', 'https://i.simpalsmedia.com/999.md/BoardImages/900x900/5f5985e8e8b5d906b1e0647e50eef880.jpg?metadata=%7B%22metadata_version%22%3A+1%2C+%22width%22%3A+1200%2C+%22height%22%3A+900%2C+%22mime_type%22%3A+%22image%2Fjpeg%22%2C+%22mime_type_extension%22%3A+%22.%22%2C+%22image_type%22%3A+%22regular%22%2C+%22signature%22%3A+%22421ecbcaaa83df25a136edf23fddc2a336f7eb92%22%7D'),
(3, '81736936', '', 'Mercedes Sprinter', 2016, NULL, 'Diesel', 'Manual', NULL, NULL, 'Albastru', '2987', NULL, '198238', NULL, '25750', NULL, '069191783', 'https://i.simpalsmedia.com/999.md/BoardImages/900x900/5f5985e8e8b5d906b1e0647e50eef880.jpg?metadata=%7B%22metadata_version%22%3A+1%2C+%22width%22%3A+1200%2C+%22height%22%3A+900%2C+%22mime_type%22%3A+%22image%2Fjpeg%22%2C+%22mime_type_extension%22%3A+%22.%22%2C+%22image_type%22%3A+%22regular%22%2C+%22signature%22%3A+%22421ecbcaaa83df25a136edf23fddc2a336f7eb92%22%7D'),
(89000641, '89000641', 'Mercedes', 'Sprinter 519 CDI', 2015, 'Republica Moldova', 'Diesel', 'Automată', 'Autofrigorifică', NULL, NULL, '2987', NULL, '272203', '4x2', '27750', NULL, '+37369191783', 'https://i.simpalsmedia.com/999.md/BoardImages/900x900/05135190d1be8fc635c5ae5eb4cb8e27.jpg');

-- --------------------------------------------------------

--
-- Structură tabel pentru tabel `car_images`
--

CREATE TABLE `car_images` (
  `id` int(11) NOT NULL,
  `car_id` int(11) DEFAULT NULL,
  `image_url` varchar(512) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Eliminarea datelor din tabel `car_images`
--

INSERT INTO `car_images` (`id`, `car_id`, `image_url`) VALUES
(1, 89000641, 'https://i.simpalsmedia.com/999.md/BoardImages/900x...1.jpg'),
(2, 89000641, 'https://i.simpalsmedia.com/999.md/BoardImages/900x...2.jpg'),
(3, 89000641, 'https://i.simpalsmedia.com/999.md/BoardImages/900x...3.jpg');

--
-- Indexuri pentru tabele eliminate
--

--
-- Indexuri pentru tabele `cars`
--
ALTER TABLE `cars`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `slug` (`slug`);

--
-- Indexuri pentru tabele `car_images`
--
ALTER TABLE `car_images`
  ADD PRIMARY KEY (`id`),
  ADD KEY `car_id` (`car_id`);

--
-- AUTO_INCREMENT pentru tabele eliminate
--

--
-- AUTO_INCREMENT pentru tabele `cars`
--
ALTER TABLE `cars`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=89000642;

--
-- AUTO_INCREMENT pentru tabele `car_images`
--
ALTER TABLE `car_images`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- Constrângeri pentru tabele eliminate
--

--
-- Constrângeri pentru tabele `car_images`
--
ALTER TABLE `car_images`
  ADD CONSTRAINT `car_images_ibfk_1` FOREIGN KEY (`car_id`) REFERENCES `cars` (`id`) ON DELETE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;

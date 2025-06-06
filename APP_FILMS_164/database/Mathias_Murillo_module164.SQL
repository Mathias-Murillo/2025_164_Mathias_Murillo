-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Host: localhost:3306
-- Generation Time: Apr 04, 2025 at 10:20 AM
-- Server version: 8.0.30
-- PHP Version: 8.1.10

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `mathias_murillo_module164`
--

-- --------------------------------------------------------
DROP DATABASE IF EXISTS Mathias_Murillo_module164;

-- Création d'un nouvelle base de donnée

CREATE DATABASE IF NOT EXISTS Mathias_Murillo_module164;

-- Utilisation de cette base de donnée

USE Mathias_Murillo_module164;
--
-- Table structure for table `fichier_utiliser`
--

CREATE TABLE `fichier_utiliser` (
  `id_fichier` int NOT NULL,
  `theme` varchar(100) NOT NULL,
  `quantité_filament` decimal(5,2) NOT NULL,
  `temp` time NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 ;

--
-- Dumping data for table `fichier_utiliser`
--

INSERT INTO `fichier_utiliser` (`id_fichier`, `theme`, `quantité_filament`, `temp`) VALUES
(1, 'pokemon', '10.00', '02:00:00'),
(2, 'deadpool', '10.00', '02:00:00');

-- --------------------------------------------------------

--
-- Table structure for table `filament`
--

CREATE TABLE `filament` (
  `filament_id` int NOT NULL,
  `nom_mat` varchar(50) DEFAULT NULL,
  `marque` varchar(50) DEFAULT NULL,
  `Taille` varchar(10) DEFAULT NULL,
  `num_serie` varchar(50) DEFAULT NULL,
  `Quantité` int DEFAULT NULL,
  `prix` decimal(8,2) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 ;

-- --------------------------------------------------------

--
-- Table structure for table `filaments_imprimante`
--

CREATE TABLE `filaments_imprimante` (
  `Imprimante_Fk` int NOT NULL,
  `Filament_Fk` int NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 ;

-- --------------------------------------------------------

--
-- Table structure for table `imprimante`
--

CREATE TABLE `imprimante` (
  `id_imprimante` int NOT NULL,
  `entretien` text,
  `marque` varchar(50) DEFAULT NULL,
  `num_serie` varchar(50) DEFAULT NULL,
  `fichier` int DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 ;

--
-- Dumping data for table `imprimante`
--

INSERT INTO `imprimante` (`id_imprimante`, `entretien`, `marque`, `num_serie`, `fichier`) VALUES
(1, 'Calibration et lubrification le 2025-03-01', 'Creality Ender 3 V2', 'SN3D123456', 1),
(2, 'Remplacement de la buse le 2025-02-15', 'Prusa i3 MK4', 'SN3D654321', 1),
(3, 'Nettoyage du plateau le 2025-02-28', 'Anycubic Photon Mono X', 'SN3D987654', 2),
(4, 'Mise à jour du firmware le 2025-01-20', 'Elegoo Mars 3', 'SN3D456789', 2),
(5, 'Vérification du système de refroidissement le 2025-03-05', 'Bambu Lab X1 Carbon', 'SN3D112233', 1),
(6, 'Remplacement du moteur Z le 2025-01-10', 'FlashForge Adventurer 4', 'SN3D998877', 2);

-- --------------------------------------------------------

--
-- Table structure for table `mat_entretien`
--

CREATE TABLE `mat_entretien` (
  `Materiel_id` int NOT NULL,
  `type_outil` varchar(50) DEFAULT NULL,
  `produit` varchar(50) DEFAULT NULL,
  `prix` decimal(8,2) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 ;

--
-- Dumping data for table `mat_entretien`
--

INSERT INTO `mat_entretien` (`Materiel_id`, `type_outil`, `produit`, `prix`) VALUES
(101, 'Pinceau', 'Nettoyant multi-surface', '5.50'),
(102, 'Chiffon', 'Alcool isopropylique', '3.20'),
(103, 'Tournevis', 'Graisse lubrifiante', '7.80'),
(104, 'Éponge', 'Détergent doux', '2.10'),
(105, 'Brosse', 'Solvant léger', '4.90'),
(106, 'Coton-tige', 'Nettoyant précision', '1.50');

-- --------------------------------------------------------

--
-- Table structure for table `personne`
--

CREATE TABLE `personne` (
  `id_personne` int NOT NULL,
  `Nom_pers` varchar(50) DEFAULT NULL,
  `prenom_pers` varchar(50) DEFAULT NULL,
  `mail_pers` varchar(100) DEFAULT NULL,
  `num_pers` varchar(15) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 ;

--
-- Dumping data for table `personne`
--

INSERT INTO `personne` (`id_personne`, `Nom_pers`, `prenom_pers`, `mail_pers`, `num_pers`) VALUES
(1, 'Dupont', 'Jean', 'jean.dupont@email.com', '0612345678'),
(2, 'Martin', 'Sophie', 'sophie.martin@email.com', '0623456789'),
(3, 'Lefevre', 'Paul', 'paul.lefevre@email.com', '0634567890'),
(4, 'Durand', 'Emma', 'emma.durand@email.com', '0645678901'),
(5, 'Bernard', 'Lucas', 'lucas.bernard@email.com', '0656789012'),
(6, 'Petit', 'Marie', 'marie.petit@email.com', '0667890123'),
(7, 'Morel', 'Thomas', 'thomas.morel@email.com', '0678901234'),
(8, 'Laurent', 'Julie', 'julie.laurent@email.com', '0689012345'),
(9, 'Simon', 'Hugo', 'hugo.simon@email.com', '0690123456'),
(10, 'Michel', 'Alice', 'alice.michel@email.com', '0611122233'),
(11, 'Garcia', 'Louis', 'louis.garcia@email.com', '0622233344'),
(12, 'Robin', 'Laura', 'laura.robin@email.com', '0633344455'),
(13, 'Clement', 'Antoine', 'antoine.clement@email.com', '0644455566'),
(14, 'Gauthier', 'Camille', 'camille.gauthier@email.com', '0655566677'),
(15, 'Adam', 'Nicolas', 'nicolas.adam@email.com', '0666677788'),
(16, 'Rey', 'Chloé', 'chloe.rey@email.com', '0677788899'),
(17, 'Fernandez', 'Mélanie', 'melanie.fernandez@email.com', '0688899900'),
(18, 'Marchand', 'Benoît', 'benoit.marchand@email.com', '0699900111'),
(19, 'Perrot', 'Elise', 'elise.perrot@email.com', '0610011223'),
(20, 'Tessier', 'Damien', 'damien.tessier@email.com', '0621122334');

-- --------------------------------------------------------

--
-- Table structure for table `reservation`
--

CREATE TABLE `reservation` (
  `id_reservation` int NOT NULL,
  `date_reservation` date NOT NULL,
  `raison` text NOT NULL,
  `photo_arrivé` blob,
  `validation` varchar(20) DEFAULT NULL,
  `personne_id` int NOT NULL,
  `date_creation` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `imprimante_id` int DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 ;

--
-- Dumping data for table `reservation`
--

INSERT INTO `reservation` (`id_reservation`, `date_reservation`, `raison`, `photo_arrivé`, `validation`, `personne_id`, `date_creation`, `imprimante_id`) VALUES
(1, '2025-03-22', 'Maintenance mensuelle', NULL, 'En attente', 15, '2025-03-21 08:30:00', 1),
(2, '2025-03-23', 'Réparation urgente', NULL, 'Validé', 2, '2025-03-21 09:15:00', 2),
(3, '2025-03-24', 'Installation nouvelle imprimante', NULL, 'Refusé', 7, '2025-03-21 10:00:00', NULL),
(4, '2025-03-25', 'Contrôle qualité', NULL, 'Validé', 12, '2025-03-21 11:30:00', 3),
(5, '2025-03-26', 'Remplacement cartouche', NULL, 'En attente', 19, '2025-03-21 13:45:00', 4),
(6, '2025-03-27', 'Test impression', NULL, 'Validé', 8, '2025-03-21 14:20:00', 1),
(7, '2025-03-28', 'Mise à jour logiciel', NULL, NULL, 1, '2025-03-21 15:00:00', 5),
(8, '2025-03-29', 'Nettoyage complet', NULL, 'Validé', 4, '2025-03-21 16:15:00', 2),
(9, '2025-03-30', 'Dépannage bourrage papier', NULL, 'En attente', 17, '2025-03-21 17:30:00', 3),
(10, '2025-03-31', 'Inspection annuelle', NULL, 'Validé', 16, '2025-03-21 18:00:00', 6),
(11, '2025-04-01', 'Changement pièce usée', NULL, 'Refusé', 20, '2025-03-21 08:45:00', 1),
(12, '2025-04-02', 'Calibration couleurs', NULL, 'Validé', 9, '2025-03-21 09:30:00', 4),
(13, '2025-04-03', 'Maintenance préventive', NULL, 'En attente', 13, '2025-03-21 10:15:00', 2),
(14, '2025-04-04', 'Réparation scanner', NULL, 'Validé', 14, '2025-03-21 11:00:00', 5),
(15, '2025-04-05', 'Test connexion réseau', NULL, NULL, 5, '2025-03-21 12:30:00', 3),
(16, '2025-04-06', 'Remplacement tambour', NULL, 'Validé', 11, '2025-03-21 13:15:00', 6),
(17, '2025-04-07', 'Mise à jour firmware', NULL, 'En attente', 18, '2025-03-21 14:00:00', 1),
(18, '2025-04-08', 'Contrôle impression recto-verso', NULL, 'Validé', 6, '2025-03-21 15:30:00', 4),
(19, '2025-04-09', 'Réparation bac papier', NULL, 'Refusé', 17, '2025-03-21 16:45:00', 2),
(20, '2025-04-10', 'Maintenance complète', NULL, 'Validé', 10, '2025-03-21 17:15:00', 5);

-- --------------------------------------------------------

--
-- Table structure for table `t_nettoyage`
--

CREATE TABLE `t_nettoyage` (
  `id_nettoyage` int NOT NULL,
  `date_net` date DEFAULT NULL,
  `mat_utiliser` int DEFAULT NULL,
  `photo_état` blob,
  `fk_personne` int DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 ;

--
-- Dumping data for table `t_nettoyage`
--

INSERT INTO `t_nettoyage` (`id_nettoyage`, `date_net`, `mat_utiliser`, `photo_état`, `fk_personne`) VALUES
(1, '2025-03-22', 101, NULL, 5),
(2, '2025-03-23', 102, NULL, 12),
(3, '2025-03-24', 103, NULL, 8),
(4, '2025-03-25', 101, NULL, 19),
(5, '2025-03-26', 104, NULL, 5),
(6, '2025-03-27', 102, NULL, 7),
(7, '2025-03-28', 105, NULL, 14),
(8, '2025-03-29', 103, NULL, 20),
(9, '2025-03-30', 106, NULL, 10),
(10, '2025-03-31', 101, NULL, 11),
(11, '2025-04-01', 104, NULL, 17),
(12, '2025-04-02', 102, NULL, 9),
(13, '2025-04-03', 105, NULL, 13),
(14, '2025-04-04', 103, NULL, 6),
(15, '2025-04-05', 106, NULL, 18),
(16, '2025-04-06', 101, NULL, 15),
(17, '2025-04-07', 104, NULL, 20),
(18, '2025-04-08', 102, NULL, 13),
(19, '2025-04-09', 105, NULL, 6),
(20, '2025-04-10', 103, NULL, 1);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `fichier_utiliser`
--
ALTER TABLE `fichier_utiliser`
  ADD PRIMARY KEY (`id_fichier`);

--
-- Indexes for table `filament`
--
ALTER TABLE `filament`
  ADD PRIMARY KEY (`filament_id`),
  ADD UNIQUE KEY `num_serie` (`num_serie`);

--
-- Indexes for table `filaments_imprimante`
--
ALTER TABLE `filaments_imprimante`
  ADD PRIMARY KEY (`Imprimante_Fk`,`Filament_Fk`),
  ADD KEY `Filament_Fk` (`Filament_Fk`);

--
-- Indexes for table `imprimante`
--
ALTER TABLE `imprimante`
  ADD PRIMARY KEY (`id_imprimante`),
  ADD UNIQUE KEY `num_serie` (`num_serie`),
  ADD KEY `fichier` (`fichier`);

--
-- Indexes for table `mat_entretien`
--
ALTER TABLE `mat_entretien`
  ADD PRIMARY KEY (`Materiel_id`);

--
-- Indexes for table `personne`
--
ALTER TABLE `personne`
  ADD PRIMARY KEY (`id_personne`),
  ADD UNIQUE KEY `mail_pers` (`mail_pers`);

--
-- Indexes for table `reservation`
--
ALTER TABLE `reservation`
  ADD PRIMARY KEY (`id_reservation`),
  ADD KEY `personne_id` (`personne_id`),
  ADD KEY `fk_imprimante` (`imprimante_id`);

--
-- Indexes for table `t_nettoyage`
--
ALTER TABLE `t_nettoyage`
  ADD PRIMARY KEY (`id_nettoyage`),
  ADD KEY `mat_utiliser` (`mat_utiliser`),
  ADD KEY `fk_t_nettoyage_personne` (`fk_personne`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `fichier_utiliser`
--
ALTER TABLE `fichier_utiliser`
  MODIFY `id_fichier` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `filament`
--
ALTER TABLE `filament`
  MODIFY `filament_id` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `imprimante`
--
ALTER TABLE `imprimante`
  MODIFY `id_imprimante` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT for table `mat_entretien`
--
ALTER TABLE `mat_entretien`
  MODIFY `Materiel_id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=107;

--
-- AUTO_INCREMENT for table `personne`
--
ALTER TABLE `personne`
  MODIFY `id_personne` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=21;

--
-- AUTO_INCREMENT for table `reservation`
--
ALTER TABLE `reservation`
  MODIFY `id_reservation` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=21;

--
-- AUTO_INCREMENT for table `t_nettoyage`
--
ALTER TABLE `t_nettoyage`
  MODIFY `id_nettoyage` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=21;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `filaments_imprimante`
--
ALTER TABLE `filaments_imprimante`
  ADD CONSTRAINT `filaments_imprimante_ibfk_1` FOREIGN KEY (`Imprimante_Fk`) REFERENCES `imprimante` (`id_imprimante`) ON DELETE CASCADE,
  ADD CONSTRAINT `filaments_imprimante_ibfk_2` FOREIGN KEY (`Filament_Fk`) REFERENCES `filament` (`filament_id`) ON DELETE CASCADE;

--
-- Constraints for table `imprimante`
--
ALTER TABLE `imprimante`
  ADD CONSTRAINT `imprimante_ibfk_1` FOREIGN KEY (`fichier`) REFERENCES `fichier_utiliser` (`id_fichier`) ON DELETE CASCADE;

--
-- Constraints for table `reservation`
--
ALTER TABLE `reservation`
  ADD CONSTRAINT `fk_imprimante` FOREIGN KEY (`imprimante_id`) REFERENCES `imprimante` (`id_imprimante`) ON DELETE SET NULL,
  ADD CONSTRAINT `reservation_ibfk_1` FOREIGN KEY (`personne_id`) REFERENCES `personne` (`id_personne`) ON DELETE CASCADE;

--
-- Constraints for table `t_nettoyage`
--
ALTER TABLE `t_nettoyage`
  ADD CONSTRAINT `fk_t_nettoyage_personne` FOREIGN KEY (`fk_personne`) REFERENCES `personne` (`id_personne`) ON DELETE CASCADE,
  ADD CONSTRAINT `t_nettoyage_ibfk_1` FOREIGN KEY (`mat_utiliser`) REFERENCES `mat_entretien` (`Materiel_id`) ON DELETE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;

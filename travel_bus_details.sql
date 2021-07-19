-- MySQL dump 10.13  Distrib 8.0.17, for Win64 (x86_64)
--
-- Host: localhost    Database: travel
-- ------------------------------------------------------
-- Server version	8.0.17

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `bus_details`
--

DROP TABLE IF EXISTS `bus_details`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `bus_details` (
  `busid` int(200) NOT NULL AUTO_INCREMENT,
  `busno` varchar(30) DEFAULT NULL,
  `busname` varchar(30) DEFAULT NULL,
  `source` varchar(30) DEFAULT NULL,
  `dest` varchar(30) DEFAULT NULL,
  `dep_time` time DEFAULT NULL,
  `avail_seats` json DEFAULT NULL,
  `ticket_price` int(9) DEFAULT NULL,
  `booked_arr` json DEFAULT NULL,
  PRIMARY KEY (`busid`)
) ENGINE=InnoDB AUTO_INCREMENT=44 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `bus_details`
--

LOCK TABLES `bus_details` WRITE;
/*!40000 ALTER TABLE `bus_details` DISABLE KEYS */;
INSERT INTO `bus_details` VALUES (31,'Ba 4 Kha 7080','Bagmati Deluxe','Biratnagar','Kathmandu','16:00:00','{}',900,'{}'),(32,'Na 3 Pa 1384','Makalu Deluxe','Biratnagar','Kathmandu','16:30:00','{}',1250,'{}'),(33,'Lu 2 Ta 5630','Lumbini Deluxe','Butwal','Ilam','15:30:00','{}',1200,'{}'),(34,'Ra 1 Ta 2522','Rapti AC','Tulsipur','Kathmandu','18:00:00','{}',1000,'{}'),(35,'Ra 4 Kha 1264','Tulsipur Deluxe','Tulsipur','Kathmandu','17:00:00','{}',1000,'{}'),(36,'Ko 3 Ta 8943','Prime Deluxe','Kathmandu','Biratnagar','16:15:00','{}',1100,'{}'),(37,'Ko 1 Ta 9019','Subidha Deluxe','Kathmandu','Biratnagar','19:00:00','{}',1000,'{}'),(38,'Na 4 Kha 5490','Rhino Deluxe','Bharatpur','Kathmandu','20:00:00','{}',800,'{}'),(39,'Na 4 Kha 2389','Facebook Deluxe','Bharatpur','Kathmandu','06:00:00','{}',700,'{}'),(40,'Ba 1 Ja 1020','Pashupati Yatayat','Kathmandu','Bharatpur','07:00:00','{}',900,'{}'),(41,'Lu 1 Dha 8765','Gandaki Ac','Kathmandu','Pokhara','15:00:00','{}',800,'{}'),(42,'Ga 3 Ka 1357','Lotus AC','Pokhara','Kathmandu','05:00:00','{}',800,'{}'),(43,'Ko 1 Pa 3264','Fifa Deluxe','Dharan','Kathmandu','16:00:00','{\"Mon\": 36.0, \"Sun\": 31}',900,'{\"Mon\": [\"None\"], \"Sun\": [\"3.4\", \"3.5\", \"4.4\", \"4.5\", \"None\"]}');
/*!40000 ALTER TABLE `bus_details` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2019-12-02 12:06:57

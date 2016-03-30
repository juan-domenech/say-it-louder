-- MySQL dump 10.13  Distrib 5.7.9, for osx10.9 (x86_64)
--
-- Host: localhost    Database: imdb
-- ------------------------------------------------------
-- Server version	5.7.11

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `games`
--

DROP TABLE IF EXISTS `games`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `games` (
  `game_id` int(4) NOT NULL AUTO_INCREMENT,
  `time_stamp` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `player_a` varchar(45) DEFAULT NULL,
  `player_b` varchar(45) DEFAULT NULL,
  `movieID` int(4) DEFAULT NULL,
  `keywords` varchar(200) DEFAULT NULL,
  PRIMARY KEY (`game_id`),
  UNIQUE KEY `player_b_UNIQUE` (`player_b`),
  UNIQUE KEY `player_a_UNIQUE` (`player_a`)
) ENGINE=InnoDB AUTO_INCREMENT=25 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `movies`
--

DROP TABLE IF EXISTS `movies`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `movies` (
  `movieID` int(4) NOT NULL,
  `title` varchar(226) NOT NULL,
  `year` year(4) NOT NULL,
  `kind` varchar(45) DEFAULT NULL,
  `episode of` varchar(226) DEFAULT NULL,
  `series year` year(4) DEFAULT NULL,
  `akas` varchar(226) DEFAULT NULL,
  `time_stamp` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`movieID`),
  UNIQUE KEY `id_UNIQUE` (`movieID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `movies_searches`
--

DROP TABLE IF EXISTS `movies_searches`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `movies_searches` (
  `movieID` int(4) NOT NULL,
  `search_id` int(4) NOT NULL,
  KEY `movieID_idx` (`movieID`),
  KEY `search_id_idx` (`search_id`),
  CONSTRAINT `movieID_fk` FOREIGN KEY (`movieID`) REFERENCES `movies` (`movieID`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `search_id_fk` FOREIGN KEY (`search_id`) REFERENCES `searches` (`search_id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `searches`
--

DROP TABLE IF EXISTS `searches`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `searches` (
  `search_id` int(4) NOT NULL AUTO_INCREMENT,
  `search` varchar(226) NOT NULL,
  `time_stamp` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`search_id`),
  UNIQUE KEY `id_UNIQUE` (`search_id`),
  UNIQUE KEY `string_UNIQUE` (`search`)
) ENGINE=InnoDB AUTO_INCREMENT=781 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2016-03-30 14:43:25

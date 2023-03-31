CREATE DATABASE  IF NOT EXISTS `somanath2023` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `somanath2023`;
-- MySQL dump 10.13  Distrib 8.0.26, for Win64 (x86_64)
--
-- Host: localhost    Database: somanath2023
-- ------------------------------------------------------
-- Server version	8.0.26

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
-- Table structure for table `acc_bal`
--

DROP TABLE IF EXISTS `acc_bal`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `acc_bal` (
  `acc_id` smallint unsigned NOT NULL,
  `acc_opn_bal_firm1` decimal(10,2) DEFAULT '0.00',
  `acc_opn_bal_firm2` decimal(10,2) DEFAULT '0.00',
  `acc_opn_bal_firm3` decimal(10,2) DEFAULT '0.00',
  `acc_cls_bal_firm1` decimal(10,2) DEFAULT '0.00',
  `acc_cls_bal_firm2` decimal(10,2) DEFAULT '0.00',
  `acc_cls_bal_firm3` decimal(10,2) DEFAULT '0.00',
  PRIMARY KEY (`acc_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `cashflow_purchase`
--

DROP TABLE IF EXISTS `cashflow_purchase`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `cashflow_purchase` (
  `trans_id` varchar(12) NOT NULL,
  `trans_acc` smallint unsigned DEFAULT NULL,
  `trans_firm_id` tinyint DEFAULT NULL,
  `trans_pur` varchar(12) DEFAULT NULL,
  `trans_amt` decimal(12,3) DEFAULT NULL,
  `amt_paid` decimal(12,3) DEFAULT NULL,
  `trans_mode` varchar(150) DEFAULT NULL,
  `trans_date` date DEFAULT NULL,
  `insert_time` datetime DEFAULT NULL,
  `insert_id` tinyint unsigned DEFAULT NULL,
  `update_time` datetime DEFAULT NULL,
  `update_id` tinyint unsigned DEFAULT NULL,
  PRIMARY KEY (`trans_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `cashflow_sales`
--

DROP TABLE IF EXISTS `cashflow_sales`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `cashflow_sales` (
  `trans_id` varchar(12) NOT NULL,
  `trans_acc` smallint unsigned DEFAULT NULL,
  `trans_sales` varchar(12) DEFAULT NULL,
  `trans_amt_firm1` decimal(12,3) DEFAULT '0.000',
  `amt_paid_firm1_cash` decimal(12,3) DEFAULT '0.000',
  `amt_paid_firm1_bank` decimal(12,3) DEFAULT '0.000',
  `trans_amt_firm2` decimal(12,3) DEFAULT '0.000',
  `amt_paid_firm2_cash` decimal(12,3) DEFAULT '0.000',
  `amt_paid_firm2_bank` decimal(12,3) DEFAULT '0.000',
  `trans_amt_firm3` decimal(12,3) DEFAULT '0.000',
  `amt_paid_firm3_cash` decimal(12,3) DEFAULT '0.000',
  `amt_paid_firm3_bank` decimal(12,3) DEFAULT '0.000',
  `bank_firm` tinyint DEFAULT '1',
  `trans_date` date DEFAULT NULL,
  `insert_time` datetime DEFAULT NULL,
  `insert_id` tinyint unsigned DEFAULT NULL,
  `update_time` datetime DEFAULT NULL,
  `update_id` tinyint unsigned DEFAULT NULL,
  PRIMARY KEY (`trans_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `max_id`
--

DROP TABLE IF EXISTS `max_id`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `max_id` (
  `purchases` int DEFAULT NULL,
  `sales` int DEFAULT NULL,
  `stocks` int DEFAULT NULL,
  `cashflow_purchase` int DEFAULT NULL,
  `cashflow_sales` int DEFAULT NULL,
  `firm1` int DEFAULT NULL,
  `firm2` int DEFAULT NULL,
  `firm3` int DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `purchases`
--

DROP TABLE IF EXISTS `purchases`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `purchases` (
  `pur_id` varchar(12) NOT NULL,
  `pur_acc` smallint unsigned DEFAULT NULL,
  `pur_firm_id` tinyint unsigned DEFAULT NULL,
  `pur_inv` varchar(20) DEFAULT NULL,
  `pur_prod_id` varchar(2000) DEFAULT NULL,
  `pur_prod_qty` varchar(2500) DEFAULT NULL,
  `pur_exp` decimal(8,2) DEFAULT NULL,
  `pur_date` date DEFAULT NULL,
  `tax_method` char(4) DEFAULT NULL,
  `insert_time` datetime DEFAULT NULL,
  `insert_id` tinyint unsigned DEFAULT NULL,
  `update_time` datetime DEFAULT NULL,
  `update_id` tinyint unsigned DEFAULT NULL,
  PRIMARY KEY (`pur_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `sales`
--

DROP TABLE IF EXISTS `sales`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `sales` (
  `sales_id` varchar(12) NOT NULL,
  `sales_ref` varchar(12) NOT NULL,
  `sales_acc` smallint unsigned DEFAULT NULL,
  `sales_prod_id` varchar(2000) DEFAULT NULL,
  `sales_pur_id` varchar(2500) DEFAULT NULL,
  `sales_prod_qty` varchar(2500) DEFAULT NULL,
  `sales_prod_sp` varchar(2500) DEFAULT NULL,
  `sale_date` date DEFAULT NULL,
  `discount` int DEFAULT '0',
  `insert_time` datetime DEFAULT NULL,
  `insert_id` tinyint unsigned DEFAULT NULL,
  `update_time` datetime DEFAULT NULL,
  `update_id` tinyint unsigned DEFAULT NULL,
  PRIMARY KEY (`sales_id`,`sales_ref`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `sales_sp`
--

DROP TABLE IF EXISTS `sales_sp`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `sales_sp` (
  `sales_id` varchar(12) NOT NULL,
  `sales_ref` varchar(12) NOT NULL,
  `prod_id` varchar(2000) DEFAULT NULL,
  `cost_price` varchar(2500) DEFAULT NULL,
  `units` varchar(3800) DEFAULT NULL,
  `sp_list` varchar(4000) DEFAULT NULL,
  `gst_value` varchar(2000) DEFAULT NULL,
  `cess_value` varchar(2000) DEFAULT NULL,
  `sales_profit` decimal(9,3) DEFAULT NULL,
  PRIMARY KEY (`sales_id`,`sales_ref`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `stocks`
--

DROP TABLE IF EXISTS `stocks`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `stocks` (
  `stk_id` varchar(12) NOT NULL,
  `stk_pur_id` varchar(12) NOT NULL,
  `stk_prod_id` mediumint unsigned NOT NULL,
  `stk_prod_qty` decimal(10,3) DEFAULT NULL,
  `stk_tot_qty` decimal(10,3) DEFAULT NULL,
  `stk_cost` decimal(10,3) DEFAULT NULL,
  `stk_sp_nml` varchar(45) DEFAULT NULL,
  `stk_sp_htl` varchar(45) DEFAULT NULL,
  `stk_sp_spl` varchar(45) DEFAULT NULL,
  `stk_sp_ang` varchar(45) DEFAULT NULL,
  `stk_exp` tinyint DEFAULT NULL,
  `stk_sup_id` varchar(12) DEFAULT NULL,
  `stk_firm_id` tinyint DEFAULT NULL,
  `insert_time` datetime DEFAULT NULL,
  `insert_id` tinyint unsigned DEFAULT NULL,
  `update_time` datetime DEFAULT NULL,
  `update_id` tinyint unsigned DEFAULT NULL,
  PRIMARY KEY (`stk_id`),
  KEY `insert_stk_idx` (`insert_id`),
  KEY `update_stk_idx` (`update_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2023-01-22 15:30:19

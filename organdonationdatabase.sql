-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1:3306
-- Generation Time: May 11, 2024 at 01:12 PM
-- Server version: 8.0.31
-- PHP Version: 8.0.26

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `organdonationdatabase`
--
CREATE DATABASE IF NOT EXISTS `organdonationdatabase` DEFAULT CHARACTER SET latin1 COLLATE latin1_swedish_ci;
USE `organdonationdatabase`;

-- --------------------------------------------------------

--
-- Table structure for table `auth_group`
--

DROP TABLE IF EXISTS `auth_group`;
CREATE TABLE IF NOT EXISTS `auth_group` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(150) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `auth_group_permissions`
--

DROP TABLE IF EXISTS `auth_group_permissions`;
CREATE TABLE IF NOT EXISTS `auth_group_permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `group_id` int NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  KEY `auth_group_permissions_group_id_b120cbf9` (`group_id`),
  KEY `auth_group_permissions_permission_id_84c5c92e` (`permission_id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `auth_permission`
--

DROP TABLE IF EXISTS `auth_permission`;
CREATE TABLE IF NOT EXISTS `auth_permission` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `content_type_id` int NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`),
  KEY `auth_permission_content_type_id_2f476e4b` (`content_type_id`)
) ENGINE=MyISAM AUTO_INCREMENT=53 DEFAULT CHARSET=latin1;

--
-- Dumping data for table `auth_permission`
--

INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES
(1, 'Can add log entry', 1, 'add_logentry'),
(2, 'Can change log entry', 1, 'change_logentry'),
(3, 'Can delete log entry', 1, 'delete_logentry'),
(4, 'Can view log entry', 1, 'view_logentry'),
(5, 'Can add permission', 2, 'add_permission'),
(6, 'Can change permission', 2, 'change_permission'),
(7, 'Can delete permission', 2, 'delete_permission'),
(8, 'Can view permission', 2, 'view_permission'),
(9, 'Can add group', 3, 'add_group'),
(10, 'Can change group', 3, 'change_group'),
(11, 'Can delete group', 3, 'delete_group'),
(12, 'Can view group', 3, 'view_group'),
(13, 'Can add user', 4, 'add_user'),
(14, 'Can change user', 4, 'change_user'),
(15, 'Can delete user', 4, 'delete_user'),
(16, 'Can view user', 4, 'view_user'),
(17, 'Can add content type', 5, 'add_contenttype'),
(18, 'Can change content type', 5, 'change_contenttype'),
(19, 'Can delete content type', 5, 'delete_contenttype'),
(20, 'Can view content type', 5, 'view_contenttype'),
(21, 'Can add session', 6, 'add_session'),
(22, 'Can change session', 6, 'change_session'),
(23, 'Can delete session', 6, 'delete_session'),
(24, 'Can view session', 6, 'view_session'),
(25, 'Can add donor', 7, 'add_donor'),
(26, 'Can change donor', 7, 'change_donor'),
(27, 'Can delete donor', 7, 'delete_donor'),
(28, 'Can view donor', 7, 'view_donor'),
(29, 'Can add recipient', 8, 'add_recipient'),
(30, 'Can change recipient', 8, 'change_recipient'),
(31, 'Can delete recipient', 8, 'delete_recipient'),
(32, 'Can view recipient', 8, 'view_recipient'),
(33, 'Can add donation', 9, 'add_donation'),
(34, 'Can change donation', 9, 'change_donation'),
(35, 'Can delete donation', 9, 'delete_donation'),
(36, 'Can view donation', 9, 'view_donation'),
(37, 'Can add organ request', 10, 'add_organrequest'),
(38, 'Can change organ request', 10, 'change_organrequest'),
(39, 'Can delete organ request', 10, 'delete_organrequest'),
(40, 'Can view organ request', 10, 'view_organrequest'),
(41, 'Can add hospital', 11, 'add_hospital'),
(42, 'Can change hospital', 11, 'change_hospital'),
(43, 'Can delete hospital', 11, 'delete_hospital'),
(44, 'Can view hospital', 11, 'view_hospital'),
(45, 'Can add transaction detail', 12, 'add_transactiondetail'),
(46, 'Can change transaction detail', 12, 'change_transactiondetail'),
(47, 'Can delete transaction detail', 12, 'delete_transactiondetail'),
(48, 'Can view transaction detail', 12, 'view_transactiondetail'),
(49, 'Can add organ transaction detail', 13, 'add_organtransactiondetail'),
(50, 'Can change organ transaction detail', 13, 'change_organtransactiondetail'),
(51, 'Can delete organ transaction detail', 13, 'delete_organtransactiondetail'),
(52, 'Can view organ transaction detail', 13, 'view_organtransactiondetail');

-- --------------------------------------------------------

--
-- Table structure for table `auth_user`
--

DROP TABLE IF EXISTS `auth_user`;
CREATE TABLE IF NOT EXISTS `auth_user` (
  `id` int NOT NULL AUTO_INCREMENT,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) NOT NULL,
  `first_name` varchar(150) NOT NULL,
  `last_name` varchar(150) NOT NULL,
  `email` varchar(254) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `auth_user_groups`
--

DROP TABLE IF EXISTS `auth_user_groups`;
CREATE TABLE IF NOT EXISTS `auth_user_groups` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `group_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_groups_user_id_group_id_94350c0c_uniq` (`user_id`,`group_id`),
  KEY `auth_user_groups_user_id_6a12ed8b` (`user_id`),
  KEY `auth_user_groups_group_id_97559544` (`group_id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `auth_user_user_permissions`
--

DROP TABLE IF EXISTS `auth_user_user_permissions`;
CREATE TABLE IF NOT EXISTS `auth_user_user_permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_user_permissions_user_id_permission_id_14a6b632_uniq` (`user_id`,`permission_id`),
  KEY `auth_user_user_permissions_user_id_a95ead1b` (`user_id`),
  KEY `auth_user_user_permissions_permission_id_1fbb5f2c` (`permission_id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `django_admin_log`
--

DROP TABLE IF EXISTS `django_admin_log`;
CREATE TABLE IF NOT EXISTS `django_admin_log` (
  `id` int NOT NULL AUTO_INCREMENT,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint UNSIGNED NOT NULL,
  `change_message` longtext NOT NULL,
  `content_type_id` int DEFAULT NULL,
  `user_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_content_type_id_c4bce8eb` (`content_type_id`),
  KEY `django_admin_log_user_id_c564eba6` (`user_id`)
) ;

-- --------------------------------------------------------

--
-- Table structure for table `django_content_type`
--

DROP TABLE IF EXISTS `django_content_type`;
CREATE TABLE IF NOT EXISTS `django_content_type` (
  `id` int NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`)
) ENGINE=MyISAM AUTO_INCREMENT=14 DEFAULT CHARSET=latin1;

--
-- Dumping data for table `django_content_type`
--

INSERT INTO `django_content_type` (`id`, `app_label`, `model`) VALUES
(1, 'admin', 'logentry'),
(2, 'auth', 'permission'),
(3, 'auth', 'group'),
(4, 'auth', 'user'),
(5, 'contenttypes', 'contenttype'),
(6, 'sessions', 'session'),
(7, 'donorapp', 'donor'),
(8, 'recipientapp', 'recipient'),
(9, 'donorapp', 'donation'),
(10, 'recipientapp', 'organrequest'),
(11, 'hospitalapp', 'hospital'),
(12, 'donorapp', 'transactiondetail'),
(13, 'recipientapp', 'organtransactiondetail');

-- --------------------------------------------------------

--
-- Table structure for table `django_migrations`
--

DROP TABLE IF EXISTS `django_migrations`;
CREATE TABLE IF NOT EXISTS `django_migrations` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=38 DEFAULT CHARSET=latin1;

--
-- Dumping data for table `django_migrations`
--

INSERT INTO `django_migrations` (`id`, `app`, `name`, `applied`) VALUES
(1, 'contenttypes', '0001_initial', '2024-05-07 09:13:54.144022'),
(2, 'auth', '0001_initial', '2024-05-07 09:13:54.658137'),
(3, 'admin', '0001_initial', '2024-05-07 09:13:54.816569'),
(4, 'admin', '0002_logentry_remove_auto_add', '2024-05-07 09:13:54.823280'),
(5, 'admin', '0003_logentry_add_action_flag_choices', '2024-05-07 09:13:54.829512'),
(6, 'contenttypes', '0002_remove_content_type_name', '2024-05-07 09:13:54.891493'),
(7, 'auth', '0002_alter_permission_name_max_length', '2024-05-07 09:13:54.924658'),
(8, 'auth', '0003_alter_user_email_max_length', '2024-05-07 09:13:54.966723'),
(9, 'auth', '0004_alter_user_username_opts', '2024-05-07 09:13:54.972646'),
(10, 'auth', '0005_alter_user_last_login_null', '2024-05-07 09:13:55.007397'),
(11, 'auth', '0006_require_contenttypes_0002', '2024-05-07 09:13:55.008404'),
(12, 'auth', '0007_alter_validators_add_error_messages', '2024-05-07 09:13:55.018044'),
(13, 'auth', '0008_alter_user_username_max_length', '2024-05-07 09:13:55.050484'),
(14, 'auth', '0009_alter_user_last_name_max_length', '2024-05-07 09:13:55.082232'),
(15, 'auth', '0010_alter_group_name_max_length', '2024-05-07 09:13:55.118469'),
(16, 'auth', '0011_update_proxy_permissions', '2024-05-07 09:13:55.124605'),
(17, 'auth', '0012_alter_user_first_name_max_length', '2024-05-07 09:13:55.158658'),
(18, 'sessions', '0001_initial', '2024-05-07 09:13:55.195118'),
(19, 'donorapp', '0001_initial', '2024-05-09 09:07:41.356353'),
(20, 'donorapp', '0002_donor_otp_donor_otp_status', '2024-05-09 09:13:57.378439'),
(21, 'recipientapp', '0001_initial', '2024-05-09 09:28:29.242758'),
(22, 'donorapp', '0003_donation', '2024-05-09 09:57:01.378146'),
(23, 'recipientapp', '0002_organrequest', '2024-05-09 11:37:21.043029'),
(24, 'hospitalapp', '0001_initial', '2024-05-09 11:45:20.941106'),
(25, 'donorapp', '0004_donation_hospital_status', '2024-05-09 12:26:30.709639'),
(26, 'recipientapp', '0003_organrequest_linked_donation_organrequest_status', '2024-05-10 05:19:23.669614'),
(27, 'donorapp', '0005_alter_donation_hospital_status', '2024-05-10 05:43:32.876460'),
(28, 'recipientapp', '0004_alter_organrequest_status', '2024-05-10 05:58:52.697205'),
(29, 'donorapp', '0006_transactiondetail', '2024-05-11 05:57:00.819787'),
(30, 'recipientapp', '0005_organtransactiondetail', '2024-05-11 07:27:34.059426'),
(31, 'recipientapp', '0006_organtransactiondetail_hospital', '2024-05-11 07:36:50.881281'),
(32, 'recipientapp', '0007_organrequest_hospital', '2024-05-11 07:48:34.366337'),
(33, 'donorapp', '0007_delete_transactiondetail', '2024-05-11 11:34:33.306271'),
(34, 'donorapp', '0008_transactiondetail', '2024-05-11 11:34:33.464303'),
(35, 'donorapp', '0009_alter_transactiondetail_value', '2024-05-11 11:57:41.966389'),
(36, 'recipientapp', '0008_delete_organtransactiondetail', '2024-05-11 12:06:46.296935'),
(37, 'recipientapp', '0009_organtransactiondetail', '2024-05-11 12:06:46.499333');

-- --------------------------------------------------------

--
-- Table structure for table `django_session`
--

DROP TABLE IF EXISTS `django_session`;
CREATE TABLE IF NOT EXISTS `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_expire_date_a5c62663` (`expire_date`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

--
-- Dumping data for table `django_session`
--

INSERT INTO `django_session` (`session_key`, `session_data`, `expire_date`) VALUES
('2803al7x3abirejbezqvjugc2s4491ow', '.eJydzj1OxDAQQOGrmJzA9kwcO90SdqGhYuksofHPiIhoIsVZCQlxd0JFT_uKT--r2zeSRnmfV3krdad5ad3YXf-qareca2t8W-6iPFF7H5X-rLW3SKDBDcx9cFyZdWIyDhwak7KxbGGgkHoMyJRNLjBkStkPaDFFealS6qZOpWyH_msWTw8aGS-IE4DhOjE6F076HPpD8dpbOASIcl3VtMqxnvf_AY_U1GurZVTWgvNRnmepRc2i7pc1f4zKYJTu-wfZ_1iV:1s5PiR:Wzn5RdPvTrWULoPKHUdEAYFIXHK2bhM4G1YTSdTA0jU', '2024-05-24 12:51:11.970393'),
('yjcc9u8aq7z0yxri1csruyg0uvjre1h3', 'eyJpZF9mb3JfaG9zcGl0YWxfYWZ0ZXJfbG9naW4iOjF9:1s5kP4:Oy0fkVR085kto7YLQeH2iXa-Lfo_js1JjT0MQ4sfCyU', '2024-05-25 10:56:34.455537'),
('zu6mhc9tfybbzae650bgxbxftgsda5w1', 'eyJpZF9mb3JfaG9zcGl0YWxfYWZ0ZXJfbG9naW4iOjF9:1s5mSS:B_fXIntA_96Vp2RiV67aGxd1zPd9q50YE7rtkAfaeKg', '2024-05-25 13:08:12.687227');

-- --------------------------------------------------------

--
-- Table structure for table `donorapp_donation`
--

DROP TABLE IF EXISTS `donorapp_donation`;
CREATE TABLE IF NOT EXISTS `donorapp_donation` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `full_name` varchar(100) NOT NULL,
  `age` int UNSIGNED NOT NULL,
  `blood_group` varchar(3) NOT NULL,
  `address` varchar(255) NOT NULL,
  `email` varchar(254) NOT NULL,
  `contact_number` varchar(15) NOT NULL,
  `organs_to_donate` json NOT NULL,
  `additional_info` longtext,
  `donor_id` bigint NOT NULL,
  `hospital_status` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `donorapp_donation_donor_id_969a9fca` (`donor_id`)
) ;

--
-- Dumping data for table `donorapp_donation`
--

INSERT INTO `donorapp_donation` (`id`, `full_name`, `age`, `blood_group`, `address`, `email`, `contact_number`, `organs_to_donate`, `additional_info`, `donor_id`, `hospital_status`) VALUES
(25, 'deep', 23, 'B+', 'information colony, hayathnagar', 'upenderbala25@gmail.com', '09666473716', '[\"Liver\", \"Heart\", \"Brain\", \"Eyes\"]', 'sdfwfe', 1, 'Completed'),
(26, 'john brother', 24, 'A+', 'lb nagar', 'johnbrother@gmail.com', '7865434789', '[\"Kidney\", \"Liver\", \"Heart\", \"Brain\", \"Eyes\"]', 'i want to donate my organs to poor for free', 2, 'Completed'),
(13, 'upender ', 22, 'AB-', 'information colony, hayathnagar', 'upenderbala5@gmail.com', '666473716', '[\"Kidney\", \"Liver\", \"Heart\", \"Lungs\", \"Brain\"]', 'testing two', 1, 'Rejected'),
(12, 'testing database', 12, 'A-', 'information colony, hayathnagar', 'upenderbala5@gmail.com', '0966647371', '[\"Heart\", \"Corneas\", \"Eyes\"]', 'testing donation transaction deatils are storing in data base or not', 1, 'Completed');

-- --------------------------------------------------------

--
-- Table structure for table `donorapp_donor`
--

DROP TABLE IF EXISTS `donorapp_donor`;
CREATE TABLE IF NOT EXISTS `donorapp_donor` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `full_name` varchar(100) NOT NULL,
  `email` varchar(254) NOT NULL,
  `password` varchar(128) NOT NULL,
  `phone_number` varchar(15) NOT NULL,
  `blood_group` varchar(3) NOT NULL,
  `address` longtext NOT NULL,
  `photo` varchar(100) DEFAULT NULL,
  `otp` varchar(6) NOT NULL,
  `otp_status` varchar(15) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=3 DEFAULT CHARSET=latin1;

--
-- Dumping data for table `donorapp_donor`
--

INSERT INTO `donorapp_donor` (`id`, `full_name`, `email`, `password`, `phone_number`, `blood_group`, `address`, `photo`, `otp`, `otp_status`) VALUES
(1, 'upender', 'upenderbala25@gmail.com', '1', '9666473716', 'O+', 'information colony, hayathnagar', 'profiles/team-2.jpg', '3129', 'Verified'),
(2, 'john', 'john@gmail.com', '1', '7865434324', 'B-', 'lb nagar , codebook ', 'profiles/13.mp4', '4534', 'Verified');

-- --------------------------------------------------------

--
-- Table structure for table `donorapp_transactiondetail`
--

DROP TABLE IF EXISTS `donorapp_transactiondetail`;
CREATE TABLE IF NOT EXISTS `donorapp_transactiondetail` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `transaction_hash` varchar(64) NOT NULL,
  `sender_address` varchar(42) NOT NULL,
  `contract_address` varchar(42) NOT NULL,
  `gas_used` bigint NOT NULL,
  `block_number` bigint NOT NULL,
  `gas_limit` bigint NOT NULL,
  `mined_on` datetime(6) NOT NULL,
  `block_hash` varchar(64) NOT NULL,
  `value` int NOT NULL,
  `donation_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `donorapp_transactiondetail_donation_id_960ab480` (`donation_id`)
) ENGINE=MyISAM AUTO_INCREMENT=3 DEFAULT CHARSET=latin1;

--
-- Dumping data for table `donorapp_transactiondetail`
--

INSERT INTO `donorapp_transactiondetail` (`id`, `transaction_hash`, `sender_address`, `contract_address`, `gas_used`, `block_number`, `gas_limit`, `mined_on`, `block_hash`, `value`, `donation_id`) VALUES
(1, '0xdee95cea24e20d3449fad5b0c7747aa30cd468f15fd2ab745dc869d0802e7d', '0xd8aD04f4F44C331feCf4669A0E9554980823cab3', '0xd8aD04f4F44C331feCf4669A0E9554980823cab3', 22368, 57, 6721975, '2024-05-11 12:01:10.000000', '0x4b9a32848751a9e83683545ef0003e7a12db0de3d57e229092d8537ea0ade9', 0, 25),
(2, '0x03736880e5f0e99cd1fe03dccbf9ff970970c0823c8f33610c9c678177b3f6', '0xd8aD04f4F44C331feCf4669A0E9554980823cab3', '0xd8aD04f4F44C331feCf4669A0E9554980823cab3', 22368, 62, 6721975, '2024-05-11 12:41:48.000000', '0xabb9856a0a059e49c4703b87b54c373fb8cae349760b0b098f0cf9148a64ee', 0, 26);

-- --------------------------------------------------------

--
-- Table structure for table `hospitalapp_hospital`
--

DROP TABLE IF EXISTS `hospitalapp_hospital`;
CREATE TABLE IF NOT EXISTS `hospitalapp_hospital` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `email` varchar(254) NOT NULL,
  `phone` varchar(15) NOT NULL,
  `password` varchar(128) NOT NULL,
  `address` longtext NOT NULL,
  `profile_image` varchar(100) DEFAULT NULL,
  `status` varchar(10) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=18 DEFAULT CHARSET=latin1;

--
-- Dumping data for table `hospitalapp_hospital`
--

INSERT INTO `hospitalapp_hospital` (`id`, `name`, `email`, `phone`, `password`, `address`, `profile_image`, `status`) VALUES
(1, 'sainath hospitals ', 'sai@gmail.com', '765654675', '1', 'hyd', 'hospital_images/footer.png', 'Approved'),
(17, 'Cityhospital', 'hospital@gmail.com', '25224354', '1', 'codebbok', 'hospital_images/real_01049.jpg', 'Rejected');

-- --------------------------------------------------------

--
-- Table structure for table `recipientapp_organrequest`
--

DROP TABLE IF EXISTS `recipientapp_organrequest`;
CREATE TABLE IF NOT EXISTS `recipientapp_organrequest` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `full_name` varchar(100) NOT NULL,
  `email` varchar(254) NOT NULL,
  `phone_number` varchar(15) NOT NULL,
  `organs_needed` varchar(500) NOT NULL,
  `urgency_level` varchar(10) NOT NULL,
  `recipient_id` bigint NOT NULL,
  `linked_donation_id` bigint DEFAULT NULL,
  `status` varchar(10) NOT NULL,
  `hospital_id` bigint DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `recipientapp_organrequest_recipient_id_4d02f588` (`recipient_id`),
  KEY `recipientapp_organrequest_linked_donation_id_0918178a` (`linked_donation_id`),
  KEY `recipientapp_organrequest_hospital_id_776c5d2d` (`hospital_id`)
) ENGINE=MyISAM AUTO_INCREMENT=10 DEFAULT CHARSET=latin1;

--
-- Dumping data for table `recipientapp_organrequest`
--

INSERT INTO `recipientapp_organrequest` (`id`, `full_name`, `email`, `phone_number`, `organs_needed`, `urgency_level`, `recipient_id`, `linked_donation_id`, `status`, `hospital_id`) VALUES
(8, 'BALA UPENDER', 'sai@gmail.com', '09666473716', 'eyes', 'high', 4, 25, 'completed', 1),
(9, 'john2', 'john2@gmail.com', '987643472', 'liver', 'medium', 5, 26, 'completed', 17);

-- --------------------------------------------------------

--
-- Table structure for table `recipientapp_organtransactiondetail`
--

DROP TABLE IF EXISTS `recipientapp_organtransactiondetail`;
CREATE TABLE IF NOT EXISTS `recipientapp_organtransactiondetail` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `transaction_hash` varchar(64) NOT NULL,
  `sender_address` varchar(42) NOT NULL,
  `contract_address` varchar(42) NOT NULL,
  `gas_used` bigint NOT NULL,
  `block_number` bigint NOT NULL,
  `gas_limit` bigint NOT NULL,
  `mined_on` datetime(6) NOT NULL,
  `block_hash` varchar(64) NOT NULL,
  `value` bigint NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `hospital_id` bigint DEFAULT NULL,
  `organ_request_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `recipientapp_organtransactiondetail_hospital_id_589cab72` (`hospital_id`),
  KEY `recipientapp_organtransactiondetail_organ_request_id_247757bf` (`organ_request_id`)
) ENGINE=MyISAM AUTO_INCREMENT=4 DEFAULT CHARSET=latin1;

--
-- Dumping data for table `recipientapp_organtransactiondetail`
--

INSERT INTO `recipientapp_organtransactiondetail` (`id`, `transaction_hash`, `sender_address`, `contract_address`, `gas_used`, `block_number`, `gas_limit`, `mined_on`, `block_hash`, `value`, `created_at`, `hospital_id`, `organ_request_id`) VALUES
(1, '0x3b786850af5269e289e1bf5baa5846f93321ee7dd63b5454591d775e708c43', '0xd8aD04f4F44C331feCf4669A0E9554980823cab3', '0xd8aD04f4F44C331feCf4669A0E9554980823cab3', 22368, 58, 6721975, '2024-05-11 12:12:38.000000', '0x8f1a8c059dfe49f3c6140c95963ed1cea7a9c06141536aa1777e9dfa23621e', 0, '2024-05-11 12:12:38.317756', 1, 8),
(2, '0x8ad765cfbb587704ea02d8008abc429f66813af8ee024fe4d571fecb86ae75', '0xd8aD04f4F44C331feCf4669A0E9554980823cab3', '0xd8aD04f4F44C331feCf4669A0E9554980823cab3', 22368, 64, 6721975, '2024-05-11 12:47:35.000000', '0xa3e0a0f63dd3919b1d06d372518382b1a4afc2b88f7c91e8be28ce8f57b942', 0, '2024-05-11 12:47:35.685311', 17, 9),
(3, '0xeb65b65e99fccdfbe57bb0a96241949a92d01a06ce2517efb43aedee6068ae', '0xd8aD04f4F44C331feCf4669A0E9554980823cab3', '0xd8aD04f4F44C331feCf4669A0E9554980823cab3', 22368, 65, 6721975, '2024-05-11 13:10:47.000000', '0xba5416fa7e84a08fbac2e147d869a7588f1666830396e51cabac7567ac5ec2', 0, '2024-05-11 13:10:47.702083', 1, 8);

-- --------------------------------------------------------

--
-- Table structure for table `recipientapp_recipient`
--

DROP TABLE IF EXISTS `recipientapp_recipient`;
CREATE TABLE IF NOT EXISTS `recipientapp_recipient` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `full_name` varchar(100) NOT NULL,
  `email` varchar(254) NOT NULL,
  `password` varchar(128) NOT NULL,
  `phone_number` varchar(15) NOT NULL,
  `address` longtext NOT NULL,
  `photo` varchar(100) DEFAULT NULL,
  `otp` varchar(6) NOT NULL,
  `otp_status` varchar(15) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `email` (`email`)
) ENGINE=MyISAM AUTO_INCREMENT=6 DEFAULT CHARSET=latin1;

--
-- Dumping data for table `recipientapp_recipient`
--

INSERT INTO `recipientapp_recipient` (`id`, `full_name`, `email`, `password`, `phone_number`, `address`, `photo`, `otp`, `otp_status`) VALUES
(4, 'codebook', 'upenderbala25@gmail.com', '1', '9666473716', 'information colony, hayathnagar', 'recipient_profiles/team-4.jpg', '8128', 'Verified'),
(5, 'ramu', 'ramu@gmail.com', '1', '8785457576', 'codebook', 'recipient_profiles/ahqqqilsxt.mp4', '4211', 'Verified');
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;

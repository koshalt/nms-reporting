DROP TABLE IF EXISTS `time_dimension`;
CREATE TABLE `time_dimension` (
  `id` INT NOT NULL,
  `day` TINYINT NULL,
  `week` TINYINT NULL,
  `month` TINYINT NULL,
  `year` SMALLINT NULL,
  `date` DATE NULL,
  PRIMARY KEY (`id`),
  INDEX `ymd` (`year` ASC, `month` ASC, `day` ASC),
  UNIQUE INDEX `dwmy` (`day` ASC, `week` ASC, `month` ASC, `year` ASC));


DROP TABLE IF EXISTS `subscriptions`;
CREATE TABLE `subscriptions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `subscriber_id` int(11) NOT NULL,
  `subscription_pack_id` int(11) DEFAULT NULL,
  `channel_id` int(11) NOT NULL,
  `operator_id` int(11) DEFAULT NULL,
  `time_id` int(11) NOT NULL,
  `subscription_id` varchar(255) DEFAULT NULL,
  `last_modified_time` timestamp NULL DEFAULT NULL,
  `subscription_status` varchar(255) DEFAULT NULL,
  `start_date` timestamp NULL DEFAULT NULL,
  `old_subscription_id` int(11) DEFAULT NULL,
  `msisdn` varchar(10) NOT NULL,
  `last_scheduled_message_date` timestamp NULL DEFAULT NULL,
  `message_campaign_pack` varchar(255) DEFAULT NULL,
  `referred_by_flw_msisdn` varchar(10) DEFAULT NULL,
  `referred_by_flag` bit(1) DEFAULT b'0',
  PRIMARY KEY (`id`),
  UNIQUE KEY `subscription_id` (`subscription_id`) USING BTREE,
  KEY `msisdn` (`msisdn`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;


DROP TABLE IF EXISTS `channel_dimension`;
CREATE TABLE `channel_dimension` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `channel` VARCHAR(255) NULL,
  PRIMARY KEY (`id`));


DROP TABLE IF EXISTS `subscribers`;
CREATE TABLE `subscribers` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(255) NULL,
  `age_of_beneficiary` INT NULL,
  `estimated_date_of_delivery` DATE NULL,
  `channel_id` INT NULL,
  `location_id` INT NULL,
  `time_id` INT NULL,
  `operator_id` INT NULL,
  `start_week_number` INT NULL,
  `last_modified_time` TIMESTAMP NULL,
  PRIMARY KEY (`id`),
  INDEX `channel_dimension_idx` (`channel_id` ASC),
  CONSTRAINT `channel_dimension`
    FOREIGN KEY (`channel_id`)
    REFERENCES `channel_dimension` (`id`)
    ON DELETE SET NULL
    ON UPDATE CASCADE);


DROP TABLE IF EXISTS `operator_dimension`;
CREATE TABLE `operator_dimension` (
  `id` INT NOT NULL,
  `operator` VARCHAR(255) NOT NULL,
  `start_pulse` INT NULL,
  `end_pulse` INT NULL,
  PRIMARY KEY (`id`));


DROP TABLE IF EXISTS `location_dimension`;
CREATE TABLE `location_dimension` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `district` VARCHAR(255) NOT NULL DEFAULT 'null',
  `block` VARCHAR(255) NOT NULL DEFAULT 'null',
  `panchayat` VARCHAR(255) NOT NULL DEFAULT 'null',
  `status` VARCHAR(36) NULL,
  `last_modified_time` TIMESTAMP NULL DEFAULT NULL,
  `alternate_location` VARCHAR(10) NULL DEFAULT 'null',
  `state` VARCHAR(255) NOT NULL DEFAULT 'null',
  PRIMARY KEY (`id`),
  UNIQUE INDEX `sdbp` (`state` ASC, `district` ASC, `block` ASC, `panchayat` ASC));


DROP TABLE IF EXISTS `hour_dimension`;
CREATE TABLE `hour_dimension` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `hour_of_day` INT NULL,
  `minute_of_hour` INT NULL,
  PRIMARY KEY (`id`));


DROP TABLE IF EXISTS `campaign_dimension`;
CREATE TABLE `campaign_dimension` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `campaign_id` VARCHAR(45) NULL,
  `obd_message_duration` INT NULL,
  `inbox_message_duration` INT NULL,
  PRIMARY KEY (`id`));

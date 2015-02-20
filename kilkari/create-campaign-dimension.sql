CREATE TABLE `kilkari`.`campaign_dimension` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `campaign_id` VARCHAR(45) NULL,
  `obd_message_duration` INT NULL,
  `inbox_message_duration` INT NULL,
  PRIMARY KEY (`id`));

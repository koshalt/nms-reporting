CREATE TABLE `kilkari`.`subscribers` (
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
    REFERENCES `kilkari`.`channel_dimension` (`id`)
    ON DELETE SET NULL
    ON UPDATE CASCADE);

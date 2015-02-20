CREATE TABLE `kilkari`.`location_dimension` (
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

CREATE TABLE `nms_reports`.`time_dimension` (
  `id` INT NOT NULL,
  `day` TINYINT NULL,
  `week` TINYINT NULL,
  `month` TINYINT NULL,
  `year` SMALLINT NULL,
  `date` DATE NULL,
  PRIMARY KEY (`id`),
  INDEX `ymd` (`year` ASC, `month` ASC, `day` ASC),
  UNIQUE INDEX `dwmy` (`day` ASC, `week` ASC, `month` ASC, `year` ASC));

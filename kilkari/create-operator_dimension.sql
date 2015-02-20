CREATE TABLE `nms_reports`.`operator_dimension` (
  `id` INT NOT NULL,
  `operator` VARCHAR(255) NOT NULL,
  `start_pulse` INT NULL,
  `end_pulse` INT NULL,
  PRIMARY KEY (`id`));

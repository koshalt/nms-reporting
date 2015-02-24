#!/usr/bin/python

import sys
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-d", "--database", help="database name", default="nms")
args = parser.parse_args()

if __name__ == '__main__':
    f = sys.stdout

    f.write("drop schema if exists {};\n".format(args.database))
    f.write("create schema {};\n".format(args.database))
    f.write("use {};\n".format(args.database))

    f.write("""
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


CREATE TABLE `channel_dimension` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `channel` VARCHAR(255) NULL,
  PRIMARY KEY (`id`));


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
  INDEX `channel_dimension_idx` (`channel_id` ASC));


CREATE TABLE `operator_dimension` (
  `id` INT NOT NULL,
  `operator` VARCHAR(255) NOT NULL,
  `start_pulse` INT NULL,
  `end_pulse` INT NULL,
  PRIMARY KEY (`id`));


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


CREATE TABLE `hour_dimension` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `hour_of_day` INT NULL,
  `minute_of_hour` INT NULL,
  PRIMARY KEY (`id`));


CREATE TABLE `campaign_dimension` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `campaign_id` VARCHAR(45) NULL,
  `obd_message_duration` INT NULL,
  `inbox_message_duration` INT NULL,
  PRIMARY KEY (`id`));

    """)

    f.write('LOCK TABLES campaign_dimension WRITE;\n')
    f.write('INSERT INTO campaign_dimension (id, campaign_id) VALUES\n')
    id = 1
    count = 2
    for campaign in range(id, count+1):
        f.write('({},"campaign{}"){}\n'.format(id, campaign, ';' if id == count else ','))
        id += 1
    f.write('UNLOCK TABLES;\n')


    f.write('LOCK TABLES channel_dimension WRITE;\n')
    f.write('INSERT INTO channel_dimension (id, channel) VALUES\n')
    id = 1
    count = 2
    for channel in range(id, count+1):
        f.write('({},"channel{}"){}\n'.format(id, channel, ';' if id == count else ','))
        id += 1
    f.write('UNLOCK TABLES;\n')
    f.write('ALTER TABLE subscribers ADD FOREIGN KEY subscribers_ibfk_1 (channel_id) REFERENCES channel_dimension(id) ON DELETE SET NULL ON UPDATE CASCADE;\n')


    f.write('LOCK TABLES hour_dimension WRITE;\n')
    f.write('INSERT INTO hour_dimension (id, hour_of_day, minute_of_hour) VALUES\n')
    id = 1
    count_hour = 24
    count_minute = 60
    count = count_hour * count_minute
    for hour in range(0,count_hour):
        for minute in range(0,count_minute):
            f.write('({},{},{}){}\n'.format(id, hour, minute, ';' if id == count else ','))
            id += 1
    f.write('UNLOCK TABLES;\n')


    f.write('LOCK TABLES location_dimension WRITE;\n')
    f.write('INSERT INTO location_dimension (id, state, district, block) VALUES\n')
    id = 1
    count_state = 40
    count_district = 10
    count_block = 10
    count = count_state * count_district * count_block
    for state in range(1,count_state+1):
        for district in range(1,count_district+1):
            for block in range(1,count_block+1):
                f.write('({}, "state{}","district{}","block{}"){}\n'.format(id, state, district, block, ';' if id == count else ','))
                id += 1
    f.write('UNLOCK TABLES;\n')


    f.write('LOCK TABLES operator_dimension WRITE;\n')
    f.write('INSERT INTO operator_dimension (id, operator) VALUES\n')
    id = 1
    count = 6
    for operator in range(1,count+1):
        f.write('({}, "operator{}"){}\n'.format(id, operator, ';' if id == count else ','))
        id += 1
    f.write('UNLOCK TABLES;\n')


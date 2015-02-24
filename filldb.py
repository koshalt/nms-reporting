#!/usr/bin/python

import sys
import argparse
import calendar
import datetime

parser = argparse.ArgumentParser()
parser.add_argument("-d", "--database", help="database name", default="nms")
parser.add_argument("--subscribers", help="number of subscribers", default=1000, type=int)
parser.add_argument("--channels", help="number of channels", default=2, type=int)
parser.add_argument("--subscription_packs", help="number of subscription packs", default=3, type=int)
parser.add_argument("--operators", help="number of operators", default=6, type=int)
parser.add_argument("--campaigns", help="number of campaigns", default=2, type=int)
parser.add_argument("--hours", help="number of hours", default=24, type=int)
parser.add_argument("--minutes", help="number of minutes", default=60, type=int)
parser.add_argument("--states", help="number of states", default=40, type=int)
parser.add_argument("--districts", help="number of districts", default=10, type=int)
parser.add_argument("--blocks", help="number of blocks", default=10, type=int)
parser.add_argument("--years", help="number of years", default=4, type=int)
args = parser.parse_args()

if __name__ == '__main__':
    f = sys.stdout

    f.write("drop schema if exists {};\n".format(args.database))
    f.write("create schema {};\n".format(args.database))
    f.write("use {};\n".format(args.database))

    f.write("""
CREATE TABLE `time_dimension` (
  `id` INT NOT NULL,
  `day` SMALLINT NULL,
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


CREATE TABLE `subscription_pack_dimension` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `subscription_pack` VARCHAR(255),
  `subscription_pack_alias` VARCHAR(255) NULL,
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

    f.write('LOCK TABLES time_dimension WRITE;\n')
    f.write('INSERT INTO time_dimension (id, day, week, month, year, date) VALUES\n')
    id = 1
    sep = ","
    this_year = datetime.date.today().year
    for year in range(this_year, this_year+args.years+1):
        day = 1
        week = 1
        for month in range(1, 13):
            last_day_of_month = calendar.monthrange(year, month)[1]
            for day_of_month in range(1, last_day_of_month+1):
                if year == this_year+args.years and month == 12 and day_of_month == last_day_of_month:
                    sep = ";"
                f.write('({},{},{},{},{},"{}-{}-{}"){}\n'.format(id, day, week, month, year, year, month, day_of_month, sep))
                id += 1
                day += 1
                if day % 7 == 0:
                    week += 1
    f.write('UNLOCK TABLES;\n')

    f.write('LOCK TABLES campaign_dimension WRITE;\n')
    f.write('INSERT INTO campaign_dimension (id, campaign_id) VALUES\n')
    id = 1
    for campaign in range(id, args.campaigns+1):
        f.write('({},"campaign{}"){}\n'.format(id, campaign, ';' if id == args.campaigns else ','))
        id += 1
    f.write('UNLOCK TABLES;\n')

    f.write('LOCK TABLES channel_dimension WRITE;\n')
    f.write('INSERT INTO channel_dimension (id, channel) VALUES\n')
    id = 1
    for channel in range(id, args.channels+1):
        f.write('({},"channel{}"){}\n'.format(id, channel, ';' if id == args.channels else ','))
        id += 1
    f.write('UNLOCK TABLES;\n')
    f.write('ALTER TABLE subscribers ADD FOREIGN KEY subscribers_ibfk_1 (channel_id) REFERENCES channel_dimension(id) ON DELETE SET NULL ON UPDATE CASCADE;\n')


    f.write('LOCK TABLES hour_dimension WRITE;\n')
    f.write('INSERT INTO hour_dimension (id, hour_of_day, minute_of_hour) VALUES\n')
    id = 1
    count_hours = args.hours * args.minutes
    for hour in range(0, args.hours):
        for minute in range(0, args.minutes):
            f.write('({},{},{}){}\n'.format(id, hour, minute, ';' if id == count_hours else ','))
            id += 1
    f.write('UNLOCK TABLES;\n')


    f.write('LOCK TABLES location_dimension WRITE;\n')
    f.write('INSERT INTO location_dimension (id, state, district, block) VALUES\n')
    id = 1
    count_dimensions = args.states*args.districts*args.blocks
    for state in range(1, args.states+1):
        for district in range(1, args.districts+1):
            for block in range(1, args.blocks+1):
                f.write('({}, "state{}","district{}","block{}"){}\n'.format(id, state, district, block, ';' if id == count_dimensions else ','))
                id += 1
    f.write('UNLOCK TABLES;\n')


    f.write('LOCK TABLES operator_dimension WRITE;\n')
    f.write('INSERT INTO operator_dimension (id, operator) VALUES\n')
    id = 1
    for operator in range(1,args.operators+1):
        f.write('({}, "operator{}"){}\n'.format(id, operator, ';' if id == args.operators else ','))
        id += 1
    f.write('UNLOCK TABLES;\n')


    f.write('LOCK TABLES subscription_pack_dimension WRITE;\n')
    f.write('INSERT INTO subscription_pack_dimension (id, subscription_pack) VALUES\n')
    id = 1
    for subscription_pack in range(id, args.subscription_packs+1):
        f.write('({},"subscription_pack{}"){}\n'.format(id, subscription_pack, ';' if id == args.subscription_packs else ','))
        id += 1
    f.write('UNLOCK TABLES;\n')


    f.write('LOCK TABLES subscribers WRITE;\n')
    f.write('INSERT INTO subscribers (id, name) VALUES\n')
    id = 1
    for subscriber in range(1, args.subscribers+1):
        f.write('({},"subscriber{}"){}\n'.format(id, subscriber, ';' if id == args.subscribers else ','))
        id += 1
    f.write('UNLOCK TABLES;\n')


    f.write('LOCK TABLES subscriptions WRITE;\n')
    f.write('INSERT INTO subscriptions (id, subscriber_id, subscription_pack_id, channel_id, time_id) VALUES\n')
    id = 1
    count_subscriptions = args.subscribers*args.subscription_packs
    for subscription_pack in range(1, args.subscription_packs+1):
        for subscriber in range(1, args.subscribers+1):
            f.write('({},{},{},{},{}){}\n'.format(id, subscriber, subscription_pack, 1, 1, ';' if id == count_subscriptions else ','))
            id += 1
    f.write('UNLOCK TABLES;\n')

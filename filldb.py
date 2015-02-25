#!/usr/bin/python

########################################################################################################################
########################################################################################################################
#
# To create a schema with 10 million subscribers, first create the schema and 1M subscribers:
#
#   $ ./filldb.py --subscribers=1000000 | mysql -u root --password=password
#
# then create a sql file to append 1M subscribers:
#
#   $ ./filldb.py --subscribers=1000000 --append > x.sql
#
# and run it 9 times:
#
#   $ for((i=1;i<=9;i+=1)); do mysql -u root --password=password < x.sql; done
#
#
#
# **************
# **   NOTE   **
# **************
#
# If you receive either of the following errors:
# IOError: [Errno 32] Broken pipe
# or
# ERROR 2006 (HY000) at line 7406: MySQL server has gone away
# Try increasing the value of the [mysqld] / max_alllowed_packet entry in /etc/mysql/my.cnf and restart mysql
#
########################################################################################################################
########################################################################################################################

import sys
import argparse
import calendar
import datetime

parser = argparse.ArgumentParser()
parser.add_argument("--database", help="database name", default="nms")
parser.add_argument("--append", help="only append to the subscriber & subscription tables", action="store_true")
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

    if not args.append:
        f.write("drop schema if exists {};\n".format(args.database))
        f.write("create schema {};\n".format(args.database))

    f.write("use {};\n".format(args.database))

    if not args.append:
        f.write("""
CREATE TABLE `time_dimension` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `day` SMALLINT,
  `week` TINYINT,
  `month` TINYINT,
  `year` SMALLINT,
  `date` DATE,
  PRIMARY KEY (`id`),
  INDEX `ymd` (`year` ASC, `month` ASC, `day` ASC),
  UNIQUE INDEX `dwmy` (`day` ASC, `week` ASC, `month` ASC, `year` ASC));


CREATE TABLE `subscriptions` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `subscriber_id` INT NOT NULL,
  `subscription_pack_id` INT,
  `channel_id` INT NOT NULL,
  `operator_id` INT,
  `time_id` INT NOT NULL,
  `subscription_id` varchar(255),
  `last_modified_time` timestamp,
  `subscription_status` varchar(255),
  `start_date` timestamp,
  `old_subscription_id` INT,
  `msisdn` varchar(10) NOT NULL,
  `last_scheduled_message_date` timestamp,
  `message_campaign_pack` varchar(255),
  `referred_by_flw_msisdn` varchar(10),
  `referred_by_flag` bit(1) DEFAULT b'0',
  PRIMARY KEY (`id`),
  UNIQUE KEY `subscription_id` (`subscription_id`) USING BTREE,
  KEY `msisdn` (`msisdn`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;


CREATE TABLE `channel_dimension` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `channel` VARCHAR(255),
  PRIMARY KEY (`id`));


CREATE TABLE `subscription_pack_dimension` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `subscription_pack` VARCHAR(255),
  `subscription_pack_alias` VARCHAR(255),
  PRIMARY KEY (`id`));


CREATE TABLE `subscribers` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(255),
  `age_of_beneficiary` INT,
  `estimated_date_of_delivery` DATE,
  `channel_id` INT,
  `location_id` INT,
  `time_id` INT,
  `operator_id` INT,
  `start_week_number` INT,
  `last_modified_time` TIMESTAMP,
  PRIMARY KEY (`id`),
  INDEX `channel_dimension_idx` (`channel_id` ASC));


CREATE TABLE `operator_dimension` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `operator` VARCHAR(255) NOT NULL,
  `start_pulse` INT,
  `end_pulse` INT,
  PRIMARY KEY (`id`));


CREATE TABLE `location_dimension` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `district` VARCHAR(255) NOT NULL,
  `block` VARCHAR(255) NOT NULL,
  `panchayat` VARCHAR(255) NOT NULL,
  `status` VARCHAR(36),
  `last_modified_time` TIMESTAMP,
  `alternate_location` VARCHAR(10),
  `state` VARCHAR(255) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `sdbp` (`state` ASC, `district` ASC, `block` ASC, `panchayat` ASC));


CREATE TABLE `hour_dimension` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `hour_of_day` INT,
  `minute_of_hour` INT,
  PRIMARY KEY (`id`));


CREATE TABLE `campaign_dimension` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `campaign_id` VARCHAR(45),
  `obd_message_duration` INT,
  `inbox_message_duration` INT,
  PRIMARY KEY (`id`));


CREATE TABLE `subscription_status_measure` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `subscription_id` INT NOT NULL,
  `status` VARCHAR(255),
  `week_number` INT,
  `channel_id` INT,
  `operator_id` INT,
  `subscription_pack_id` INT,
  `remarks` VARCHAR(255),
  `grace_count` INT,
  `date_id` INT,
  `last_modified_time` TIMESTAMP,
  `mode` VARCHAR(255),
  PRIMARY KEY (`id`));


CREATE TABLE `subscriber_call_measure` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `subscription_id` INT NOT NULL,
  `call_status` VARCHAR(255),
  `duration` INT,
  `operator_id` INT,
  `subscription_pack_id` INT,
  `service_option` VARCHAR(255),
  `percentage_listened` TINYINT,
  `campaign_id` INT,
  `state_date` INT,
  `end_date` INT,
  `start_time` INT,
  `end_time` INT,
  `call_source` VARCHAR(255),
  `subscription_status` VARCHAR(255),
  `duration_in_pulse` INT,
  PRIMARY KEY (`id`));


    """)

        f.write('LOCK TABLES time_dimension WRITE;\n')
        f.write('INSERT INTO time_dimension (day, week, month, year, date) VALUES\n')
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
                    f.write('({},{},{},{},"{}-{}-{}"){}\n'.format(day, week, month, year, year, month, day_of_month, sep))
                    day += 1
                    if day % 7 == 0:
                        week += 1
        f.write('UNLOCK TABLES;\n')

        f.write('LOCK TABLES campaign_dimension WRITE;\n')
        f.write('INSERT INTO campaign_dimension (campaign_id) VALUES\n')
        for campaign in range(1, args.campaigns+1):
            f.write('("campaign{}"){}\n'.format(campaign, ';' if campaign == args.campaigns else ','))
        f.write('UNLOCK TABLES;\n')

        f.write('LOCK TABLES channel_dimension WRITE;\n')
        f.write('INSERT INTO channel_dimension (channel) VALUES\n')
        for channel in range(1, args.channels+1):
            f.write('("channel{}"){}\n'.format(channel, ';' if channel == args.channels else ','))
        f.write('UNLOCK TABLES;\n')


        f.write('LOCK TABLES hour_dimension WRITE;\n')
        f.write('INSERT INTO hour_dimension (hour_of_day, minute_of_hour) VALUES\n')
        count_hours = args.hours * args.minutes
        count = 1
        for hour in range(0, args.hours):
            for minute in range(0, args.minutes):
                f.write('({},{}){}\n'.format(hour, minute, ';' if count == count_hours else ','))
                count += 1
        f.write('UNLOCK TABLES;\n')

        f.write('LOCK TABLES location_dimension WRITE;\n')
        f.write('INSERT INTO location_dimension (state, district, block) VALUES\n')
        count = 1
        count_dimensions = args.states*args.districts*args.blocks
        for state in range(1, args.states+1):
            for district in range(1, args.districts+1):
                for block in range(1, args.blocks+1):
                    f.write('("state{}","district{}","block{}"){}\n'.format(state, district, block, ';' if count == count_dimensions else ','))
                    count += 1
        f.write('UNLOCK TABLES;\n')

        f.write('LOCK TABLES operator_dimension WRITE;\n')
        f.write('INSERT INTO operator_dimension (operator) VALUES\n')
        for operator in range(1,args.operators+1):
            f.write('("operator{}"){}\n'.format(operator, ';' if operator == args.operators else ','))
        f.write('UNLOCK TABLES;\n')

        f.write('LOCK TABLES subscription_pack_dimension WRITE;\n')
        f.write('INSERT INTO subscription_pack_dimension (subscription_pack) VALUES\n')
        for subscription_pack in range(1, args.subscription_packs+1):
            f.write('("subscription_pack{}"){}\n'.format(subscription_pack, ';' if subscription_pack == args.subscription_packs else ','))
        f.write('UNLOCK TABLES;\n')

    f.write('SET @x=(SELECT IFNULL((SELECT MAX(id) FROM subscribers), 1));\n')
    f.write('LOCK TABLES subscribers WRITE;\n')
    f.write('INSERT INTO subscribers (name) VALUES\n')
    for subscriber in range(1, args.subscribers+1):
        f.write('(CONCAT("subscriber", @x+{})){}\n'.format(subscriber, ';' if subscriber == args.subscribers else ','))
    f.write('UNLOCK TABLES;\n')

    f.write('SET @x=(SELECT IFNULL((SELECT MAX(id) FROM subscriptions), 1));\n')
    f.write('LOCK TABLES subscriptions WRITE;\n')
    f.write('INSERT INTO subscriptions (subscriber_id, subscription_pack_id, channel_id, time_id) VALUES\n')
    count = 1
    count_subscriptions = args.subscribers*args.subscription_packs
    for subscription_pack in range(1, args.subscription_packs+1):
        for subscriber in range(1, args.subscribers+1):
            f.write('(@x+{},{},{},{}){}\n'.format(subscriber, subscription_pack, 1, 1, ';' if count == count_subscriptions else ','))
            count += 1
    f.write('UNLOCK TABLES;\n')

    f.write('SET @x=(SELECT IFNULL((SELECT MAX(id) FROM subscription_status_measure), 1));\n')
    f.write('LOCK TABLES subscription_status_measure WRITE;\n')
    f.write('INSERT INTO subscription_status_measure (subscribtion_id, subscription_pack_id, channel_id, time_id) VALUES\n')
    count = 1
    count_subscriptions = args.subscribers*args.subscription_packs
    for subscription_pack in range(1, args.subscription_packs+1):
        for subscriber in range(1, args.subscribers+1):
            f.write('(@x+{},{},{},{}){}\n'.format(subscriber, subscription_pack, 1, 1, ';' if count == count_subscriptions else ','))
            count += 1
    f.write('UNLOCK TABLES;\n')

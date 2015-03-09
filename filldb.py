#!/usr/bin/python

#################################################################################################
#################################################################################################
#
# To create a schema with 1 million subscribers, first create the schema and 1M subscribers:
#
#   $ ./filldb.py --subscribers=1000000 --max-inserts 50000 | mysql -u root --password=password
#
# **************
# **   NOTE   **
# **************
#
# If you receive either of the following errors:
# IOError: [Errno 32] Broken pipe
# or
# ERROR 2006 (HY000) at line 7406: MySQL server has gone away
# Try increasing the value of the [mysqld] / max_alllowed_packet entry 
#    in /etc/mysql/my.cnf and restart mysql 
#    or executing this on the server 'set global max_allowed_packet=1073741824;'
#
#################################################################################################
#################################################################################################

import sys
import argparse
import calendar
import datetime
import random

from faker import Faker
fake = Faker()
fake_IN = Faker('hi_IN')

parser = argparse.ArgumentParser()
parser.add_argument("--file-name", help="the file to write output to", default="nms.sql", dest='file_name')
parser.add_argument("--database", help="database name", default="nms")
parser.add_argument("--subscribers", help="number of subscribers", default=1000, type=int)
parser.add_argument("--channels", help="number of channels", default=2, type=int)
parser.add_argument("--subscription_packs", help="number of subscription packs", default=2, type=int)
parser.add_argument("--operators", help="number of operators", default=6, type=int)
parser.add_argument("--campaigns", help="number of campaigns", default=2, type=int)
parser.add_argument("--hours", help="number of hours", default=24, type=int)
parser.add_argument("--minutes", help="number of minutes", default=60, type=int)
parser.add_argument("--states", help="number of states", default=40, type=int)
parser.add_argument("--districts", help="number of districts", default=10, type=int)
parser.add_argument("--blocks", help="number of blocks", default=10, type=int)
parser.add_argument("--years", help="number of years", default=4, type=int)
parser.add_argument("--max-inserts", help="max number of items to insert at a time", default=1000, type=int, dest='max_inserts')
args = parser.parse_args()

if __name__ == '__main__':
    max_time_dimension_id = 0

    f = sys.stdout

    f.write("drop schema if exists {};\n".format(args.database))
    f.write("create schema {};\n".format(args.database))

    f.write("use {};\n".format(args.database))

    f.write("""
/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_AUTOCOMMIT=@@AUTOCOMMIT, AUTOCOMMIT=0 */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

CREATE TABLE `time_dimension` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `day` SMALLINT,
  `week` TINYINT,
  `month` TINYINT,
  `year` SMALLINT,
  `date` DATE,
  PRIMARY KEY (`id`),
  INDEX `ymd` (`year` ASC, `month` ASC, `day` ASC),
  UNIQUE INDEX `dwmy` (`day` ASC, `week` ASC, `month` ASC, `year` ASC)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;


CREATE TABLE `channel_dimension` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `channel` VARCHAR(255),
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;


CREATE TABLE `subscription_pack_dimension` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `subscription_pack` VARCHAR(255),
  `subscription_pack_alias` VARCHAR(255),
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;


CREATE TABLE `operator_dimension` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `operator` VARCHAR(255) NOT NULL,
  `start_pulse` INT,
  `end_pulse` INT,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;


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
  UNIQUE INDEX `sdbp` (`state` ASC, `district` ASC, `block` ASC, `panchayat` ASC)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;


CREATE TABLE `hour_dimension` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `hour_of_day` INT,
  `minute_of_hour` INT,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;


CREATE TABLE `campaign_dimension` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `campaign_id` VARCHAR(45),
  `obd_message_duration` INT,
  `inbox_message_duration` INT,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;


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
  INDEX `subscribers_location_id_idx` (`location_id` ASC),
  CONSTRAINT `fk_subscribers_channel_dimension`
    FOREIGN KEY (`channel_id`) 
    REFERENCES `channel_dimension` (`id`),
  CONSTRAINT `fk_subscribers_location_dimension`
    FOREIGN KEY (`location_id`) 
    REFERENCES `location_dimension` (`id`),
  CONSTRAINT `fk_subscribers_time_dimension`
    FOREIGN KEY (`time_id`) 
    REFERENCES `time_dimension` (`id`),
  CONSTRAINT `fk_subscribers_operator_dimension`
    FOREIGN KEY (`operator_id`) 
    REFERENCES `operator_dimension` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;


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
  `msisdn` varchar(15) NOT NULL,
  `last_scheduled_message_date` timestamp,
  `message_campaign_pack` varchar(255),
  `referred_by_flw_msisdn` varchar(10),
  `referred_by_flag` bit(1) DEFAULT b'0',
  PRIMARY KEY (`id`),
  INDEX `msisdn` (`msisdn`),
  CONSTRAINT `fk_subscriptions_subscribers`
    FOREIGN KEY (`subscriber_id`) 
    REFERENCES `subscribers` (`id`),
  CONSTRAINT `fk_subscriptions_subscription_pack_dimension`
    FOREIGN KEY (`subscription_pack_id`) 
    REFERENCES `subscription_pack_dimension` (`id`),
  CONSTRAINT `fk_subscriptions_channel_dimension`
    FOREIGN KEY (`channel_id`) 
    REFERENCES `channel_dimension` (`id`),
  CONSTRAINT `fk_subscriptions_operator_dimension`
    FOREIGN KEY (`operator_id`) 
    REFERENCES `operator_dimension` (`id`),
  CONSTRAINT `fk_subscriptions_time_dimension`
    FOREIGN KEY (`time_id`) 
    REFERENCES `time_dimension` (`id`),
  CONSTRAINT `fk_subscriptions_old_subscription`
    FOREIGN KEY (`old_subscription_id`) 
    REFERENCES `subscriptions` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;


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
  `time_id` INT,
  `hour_id` INT,
  `last_modified_time` TIMESTAMP,
  `mode` VARCHAR(255),
  PRIMARY KEY (`id`),
  INDEX `lastmodifiedtime_subscriptionid` (`last_modified_time` ASC, `subscription_id` ASC),
  INDEX `subscriptionid_status` (`subscription_id` ASC, `status` ASC),
  CONSTRAINT `subscription_status_measure_subscription_id_fkey`
    FOREIGN KEY (`subscription_id`) 
    REFERENCES `subscriptions` (`id`),
  CONSTRAINT `fk_subscription_status_measure_channel_dimension`
    FOREIGN KEY (`channel_id`) 
    REFERENCES `channel_dimension` (`id`),
  CONSTRAINT `fk_subscription_status_measure_operator_dimension`
    FOREIGN KEY (`operator_id`)
    REFERENCES `operator_dimension` (`id`),
  CONSTRAINT `fk_subscription_status_measure_subscription_pack_dimension`
    FOREIGN KEY (`subscription_pack_id`) 
    REFERENCES `subscription_pack_dimension` (`id`),
  CONSTRAINT `fk_subscription_status_measure_time_dimension`
    FOREIGN KEY (`time_id`)
    REFERENCES `time_dimension` (`id`),
  CONSTRAINT `fk_subscription_status_measure_hour_dimension`
    FOREIGN KEY (`hour_id`)
    REFERENCES `hour_dimension` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;


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
  `start_date` INT,
  `end_date` INT,
  `start_time` INT,
  `end_time` INT,
  `call_source` VARCHAR(255),
  `subscription_status` VARCHAR(255),
  `duration_in_pulse` INT,
  PRIMARY KEY (`id`),
  CONSTRAINT `fk_subscriber_call_measure_operator_dimension`
    FOREIGN KEY (`operator_id`)
    REFERENCES `operator_dimension` (`id`),
  CONSTRAINT `fk_subscriber_call_measure_subscription_pack_dimension`
    FOREIGN KEY (`subscription_pack_id`) 
    REFERENCES `subscription_pack_dimension` (`id`),
  CONSTRAINT `fk_subscriber_call_measure_campaign_dimension`
    FOREIGN KEY (`campaign_id`)
    REFERENCES `campaign_dimension` (`id`),
  CONSTRAINT `subscriber_call_measure_start_date_fkey`
    FOREIGN KEY (`start_date`)
    REFERENCES `time_dimension` (`id`),
  CONSTRAINT `subscriber_call_measure_start_time_fkey`
    FOREIGN KEY (`start_time`)
    REFERENCES `hour_dimension` (`id`),
  CONSTRAINT `subscriber_call_measure_end_date_fkey`
    FOREIGN KEY (`end_date`)
    REFERENCES `time_dimension` (`id`),
  CONSTRAINT `subscriber_call_measure_end_time_fkey`
    FOREIGN KEY (`end_time`)
    REFERENCES `hour_dimension` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

    """)

    f.write('LOCK TABLES time_dimension WRITE;\n')
    f.write('/*!40000 ALTER TABLE `time_dimension` DISABLE KEYS */;\n')
    f.write('INSERT INTO time_dimension (day, week, month, year, date) VALUES\n')
    sep = ","
    this_year = datetime.date.today().year
    for year in range(this_year, this_year+args.years+1):
        day = 1
        week = 1
        for month in range(1, 13):
            last_day_of_month = calendar.monthrange(year, month)[1]
            for day_of_month in range(1, last_day_of_month+1):
                max_time_dimension_id += 1
                if year == this_year+args.years and month == 12 and day_of_month == last_day_of_month:
                    sep = ";"
                f.write('({},{},{},{},"{}-{}-{}"){}\n'.format(day, week, month, year, year, month, day_of_month, sep))
                day += 1
                if day % 7 == 0:
                    week += 1
    f.write('/*!40000 ALTER TABLE `time_dimension` ENABLE KEYS */;\n')
    f.write('UNLOCK TABLES;\n')


    f.write('LOCK TABLES campaign_dimension WRITE;\n')
    f.write('/*!40000 ALTER TABLE `campaign_dimension` DISABLE KEYS */;\n')
    f.write('INSERT INTO campaign_dimension (campaign_id) VALUES\n')
    for campaign in range(1, args.campaigns+1):
        f.write('("campaign{}"){}\n'.format(campaign, ';' if campaign == args.campaigns else ','))
    f.write('/*!40000 ALTER TABLE `campaign_dimension` ENABLE KEYS */;\n')
    f.write('UNLOCK TABLES;\n')


    f.write('LOCK TABLES channel_dimension WRITE;\n')
    f.write('/*!40000 ALTER TABLE `channel_dimension` DISABLE KEYS */;\n')
    f.write('INSERT INTO channel_dimension (channel) VALUES\n')
    for channel in range(1, args.channels+1):
        f.write('("channel{}"){}\n'.format(channel, ';' if channel == args.channels else ','))

    f.write('/*!40000 ALTER TABLE `channel_dimension` ENABLE KEYS */;\n')
    f.write('UNLOCK TABLES;\n')


    f.write('LOCK TABLES hour_dimension WRITE;\n')
    f.write('/*!40000 ALTER TABLE `hour_dimension` DISABLE KEYS */;\n')
    f.write('INSERT INTO hour_dimension (hour_of_day, minute_of_hour) VALUES\n')
    count_hours = args.hours * args.minutes
    count = 1
    for hour in range(0, args.hours):
        for minute in range(0, args.minutes):
            f.write('({},{}){}\n'.format(hour, minute, ';' if count == count_hours else ','))
            count += 1

    f.write('/*!40000 ALTER TABLE `hour_dimension` ENABLE KEYS */;\n')
    f.write('UNLOCK TABLES;\n')

    
    f.write('LOCK TABLES location_dimension WRITE;\n')
    f.write('/*!40000 ALTER TABLE `location_dimension` DISABLE KEYS */;\n')
    f.write('INSERT INTO location_dimension (state, district, block, panchayat) VALUES\n')
    count = 1
    count_dimensions = args.states*args.districts*args.blocks
    for state in range(1, args.states+1):
        for district in range(1, args.districts+1):
            for block in range(1, args.blocks+1):
                f.write('("state{}","district{}","block{}","panchayat{}"){}\n'.format(state, district, block, 1, ';' if count == count_dimensions else ','))
                count += 1

    f.write('/*!40000 ALTER TABLE `location_dimension` ENABLE KEYS */;\n')
    f.write('UNLOCK TABLES;\n')


    f.write('LOCK TABLES operator_dimension WRITE;\n')
    f.write('/*!40000 ALTER TABLE `operator_dimension` DISABLE KEYS */;\n')
    f.write('INSERT INTO operator_dimension (operator) VALUES\n')
    for operator in range(1,args.operators+1):
        f.write('("operator{}"){}\n'.format(operator, ';' if operator == args.operators else ','))

    f.write('/*!40000 ALTER TABLE `operator_dimension` ENABLE KEYS */;\n')
    f.write('UNLOCK TABLES;\n')


    f.write('LOCK TABLES subscription_pack_dimension WRITE;\n')
    f.write('/*!40000 ALTER TABLE `subscription_pack_dimension` DISABLE KEYS */;\n')
    f.write('INSERT INTO subscription_pack_dimension (subscription_pack) VALUES\n')
    for subscription_pack in range(1, args.subscription_packs+1):
        f.write('("subscription_pack{}"){}\n'.format(subscription_pack, ';' if subscription_pack == args.subscription_packs else ','))
        
    f.write('/*!40000 ALTER TABLE `subscription_pack_dimension` ENABLE KEYS */;\n')
    f.write('UNLOCK TABLES;\n')


    insert_count = 0
    f.write('LOCK TABLES subscribers WRITE;\n')
    f.write('/*!40000 ALTER TABLE `subscribers` DISABLE KEYS */;\n')
    for subscriber in range(1, args.subscribers+1):

        if insert_count == 0:
            f.write('INSERT INTO subscribers (name) VALUES\n')

        f.write('("{}"){}\n'.format(fake.name(), 
                                    ';' if insert_count == args.max_inserts or subscriber == args.subscribers else ','))

        if insert_count == args.max_inserts or subscriber == args.subscribers:
            insert_count = 0
        else:
            insert_count += 1

    f.write('/*!40000 ALTER TABLE `subscribers` ENABLE KEYS */;\n')
    f.write('UNLOCK TABLES;\n')

    count = 1
    insert_count = 0
    count_subscriptions = args.subscribers*args.subscription_packs
    f.write('LOCK TABLES subscriptions WRITE;\n')
    f.write('/*!40000 ALTER TABLE `subscriptions` DISABLE KEYS */;\n')
    for subscription_pack_id in range(1, args.subscription_packs+1):
        for subscriber_id in range(1, args.subscribers+1):

            if insert_count == 0:
                f.write('INSERT INTO subscriptions (subscriber_id, subscription_pack_id, channel_id, time_id, msisdn) VALUES\n')

            f.write('({},{},{},{},"{}"){}\n'.format(subscriber_id, subscription_pack_id, 
                                                    random.randint(1, args.channels), 
                                                    random.randint(1, max_time_dimension_id),
                                                    fake_IN.phone_number(),
                                                    ';' if insert_count == args.max_inserts or count == count_subscriptions else ','))

            if insert_count == args.max_inserts or count == count_subscriptions:
                insert_count = 0
            else:
                insert_count += 1

            count += 1

    f.write('/*!40000 ALTER TABLE `subscriptions` ENABLE KEYS */;\n')
    f.write('UNLOCK TABLES;\n')

    insert_count = 0
    count = 1
    count_subscriptions = args.subscribers*args.subscription_packs
    f.write('LOCK TABLES subscription_status_measure WRITE;\n')
    f.write('/*!40000 ALTER TABLE `subscription_status_measure` DISABLE KEYS */;\n')
    for subscription_pack_id in range(1, args.subscription_packs+1):
        for subscriber_id in range(1, args.subscribers+1):
            
            if insert_count == 0:
                f.write('INSERT INTO subscription_status_measure (subscription_id, status, week_number, channel_id, operator_id, subscription_pack_id, remarks, time_id, hour_id) VALUES\n')

            f.write('({},"{}",{},{},{},{},{},{},{}),\n'.format(count, 
                                                           'PENDING',
                                                           random.randint(0, 40), 
                                                           random.randint(1, args.channels),
                                                           random.randint(1, args.operators),
                                                           subscription_pack_id,
                                                           '"' + fake.text(max_nb_chars=200) + '"' if random.randint(0, 5) == 0 else "null",
                                                           random.randint(1, max_time_dimension_id/3),
                                                           random.randint(1, count_hours)))

            f.write('({},"{}",{},{},{},{},{},{},{}),\n'.format(count, 
                                                           'ACTIVE',
                                                           random.randint(0, 40), 
                                                           random.randint(1, args.channels), 
                                                           random.randint(1, args.operators),
                                                           subscription_pack_id,
                                                           '"' + fake.text(max_nb_chars=200) + '"' if random.randint(0, 5) == 0 else "null",
                                                           random.randint(max_time_dimension_id/3, 
                                                                          2*(max_time_dimension_id/3)),
                                                           random.randint(1, count_hours)))

            f.write('({},"{}",{},{},{},{},{},{},{}){}\n'.format(count, 
                                                           random.choice(['DISABLED',
                                                                          'COMPLETE']), 
                                                           random.randint(0, 40), 
                                                           random.randint(1, args.channels), 
                                                           random.randint(1, args.operators),
                                                           subscription_pack_id,
                                                           '"' + fake.text(max_nb_chars=200) + '"' if random.randint(0, 5) == 0 else "null",

                                                           random.randint(2*(max_time_dimension_id/3), 
                                                                          max_time_dimension_id),
                                                           random.randint(1, count_hours),
                                                           ';' if insert_count >= args.max_inserts or count == count_subscriptions else ','))

            if insert_count >= args.max_inserts or count == count_subscriptions:
                insert_count = 0
            else:
                insert_count += 3
            count += 1

    f.write('/*!40000 ALTER TABLE `subscription_status_measure` ENABLE KEYS */;\n')
    f.write('UNLOCK TABLES;\n')

    insert_count = 0
    sub_count = 1
    f.write('LOCK TABLES subscriber_call_measure WRITE;\n')
    f.write('/*!40000 ALTER TABLE `subscriber_call_measure` DISABLE KEYS */;\n')
    for subscription_pack_id in range(1, args.subscription_packs+1):
        for subscriber_id in range(1, args.subscribers+1):
            
            subscription_id = sub_count
            operator_id = random.randint(1, args.operators)
            campaign_id = random.randint(1, args.campaigns)

            # I assume half the users will be in the 42 week pack and the other half in the 72
            if random.randint(0,1):
                min_calls = 42
                max_calls = 42 * 3
            else:
                min_calls = 72
                max_calls = 72 * 3

            call_count = random.randint(min_calls, max_calls) 
            for count in range(1, call_count+1):

                if insert_count == 0:
                    f.write('INSERT INTO subscriber_call_measure (subscription_id, call_status, duration, operator_id, subscription_pack_id, percentage_listened, campaign_id, start_date, end_date, start_time, end_time, subscription_status, duration_in_pulse) VALUES\n')

                # Some calls may span an hour boundary.  I'm not going to model that
                start_date = random.randint(1, max_time_dimension_id)
                end_date = start_date
                start_hour = random.randint(1, count_hours-2)
                end_hour = start_hour + 2
                f.write('({},"{}",{},{},{},{},{},{},{},{},{},"{}",{}){}\n'
                        .format(subscription_id,
                                random.choice(['SUCCESS', 'NOT_ANSWERED', 'SWITCHED_OFF', 'OTHER']),
                                random.randint(1, 120),
                                operator_id,
                                subscription_pack_id,
                                random.randint(1, 11),
                                campaign_id,
                                start_date,
                                end_date,
                                start_hour,
                                end_hour,
                                random.choice(['PENDING', 'ACITVE', 'DISABLED', 'CANCELLED']),
                                random.randint(1, 60),
                                ';' if insert_count == args.max_inserts or count == call_count else ','))

                if insert_count == args.max_inserts or count == call_count:
                    insert_count = 0
                else:
                    insert_count += 1

            sub_count += 1

    f.write('/*!40000 ALTER TABLE `subscriber_call_measure` ENABLE KEYS */;\n')
    f.write('UNLOCK TABLES;\n')

    f.write('COMMIT;\n')

    f.write("""
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;
/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET AUTOCOMMIT=@OLD_AUTOCOMMIT */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;
""")

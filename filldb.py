#!/usr/bin/python

import sys

if __name__ == '__main__':
    f = sys.stdout

    f.write('TRUNCATE TABLE campaign_dimension;\n')
    f.write('LOCK TABLES campaign_dimension WRITE;\n')
    f.write('INSERT INTO campaign_dimension (id, campaign_id, obd_message_duration, inbox_message_duration) VALUES\n')
    f.write('(1,"mother",NULL,NULL),\n')
    f.write('(2,"child",NULL,NULL);\n')
    f.write('UNLOCK TABLES;\n')


    f.write('ALTER TABLE subscribers DROP FOREIGN KEY channel_dimension;\n')
    f.write('TRUNCATE TABLE channel_dimension;\n')
    f.write('LOCK TABLES channel_dimension WRITE;\n')
    f.write('INSERT INTO channel_dimension (id, channel) VALUES\n')
    f.write('(1,"IVR"),\n')
    f.write('(2,"Call Center");\n')
    f.write('UNLOCK TABLES;\n')
    f.write('ALTER TABLE subscribers ADD FOREIGN KEY channel_dimension (channel_id) REFERENCES channel_dimension(id) ON DELETE SET NULL ON UPDATE CASCADE;\n')

    f.write('TRUNCATE TABLE hour_dimension;\n')
    f.write('LOCK TABLES hour_dimension WRITE;\n')
    f.write('INSERT INTO hour_dimension (id, hour_of_day, minute_of_hour) VALUES\n')
    id = 1
    for hour in range(0,24):
        for minute in range(0,60):
            f.write('({},{},{}){}\n'.format(id, hour, minute, ';' if id==1440 else ','))
            id += 1
    f.write('UNLOCK TABLES;\n')

    f.write('TRUNCATE TABLE location_dimension;\n')
    f.write('LOCK TABLES location_dimension WRITE;\n')
    f.write('INSERT INTO location_dimension (id, district, block, panchayat, status, last_modified_time, alternate_location, state) VALUES\n')
    id = 1
    for state in range(1,11):
        for district in range(1,11):
            for block in range(1,11):
                for panchayat in range(1,5):
                    f.write('({}, "state{}","district{}","block{}","panchayat{}",{},{},{}){}\n'.format(id, state, district, block, panchayat, "NULL", "NULL", "NULL", ';' if id==4000 else ','))
                    id += 1
    f.write('UNLOCK TABLES;\n')


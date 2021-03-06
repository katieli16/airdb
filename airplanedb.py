#!~/usr/bin/python
import MySQLdb
from datetime import datetime
from datetime import timedelta
from flask import jsonify
import json


class AirplaneDb(object):

    def __init__(self,host='',user='',pw='',db=''):
        self.host = host
        self.user = user
        self.pw = pw
        self.db = db

        self.airdb = MySQLdb.connect(host=self.host,
                                     user=self.user,
                                     passwd=self.pw,
                                     db=self.db)

    '''
    EXAMPLE
    function: reset_db
    description: delete all tables in airdb and recreate
    notes: need to do in this order bc the tables are key-dependent
    '''
    def reset_db(self):
        db = MySQLdb.connect(host=self.host,
                                 user=self.user,
                                 passwd=self.pw,
                                 db=self.db)
        cursor = db.cursor()
        drop = 'DROP TABLE IF EXISTS {}'
        cursor.execute(drop.format('SCHEDULE'))
        cursor.execute(drop.format('WORKSON'))
        cursor.execute(drop.format('FREQUENTFLIER'))
        cursor.execute(drop.format('BAGGAGE'))
        cursor.execute(drop.format('ITINERARY'))
        cursor.execute(drop.format('EMPLOYEE'))
        cursor.execute(drop.format('FLIGHT'))
        cursor.execute(drop.format('AIRCRAFT'))
        cursor.execute(drop.format('GATE'))
        cursor.execute(drop.format('AIRPORT'))
        cursor.execute(drop.format('CUSTOMER'))

        create_customer_table = """CREATE TABLE CUSTOMER (
                                C_ID INT AUTO_INCREMENT,
                                C_NAME VARCHAR(32) NOT NULL,
                                C_AGE INT NOT NULL,
                                C_EMAIL VARCHAR(128) NOT NULL,
                                C_PHONE VARCHAR(32) NOT NULL,
                                PRIMARY KEY (C_ID)
                                )"""

        create_airport_table = """CREATE TABLE AIRPORT (
                                AP_ID VARCHAR(32),
                                AP_CITY VARCHAR(32) NOT NULL,
                                AP_COUNTRY VARCHAR(32) NOT NULL,
                                PRIMARY KEY (AP_ID)
                                )"""

        create_gate_table = """CREATE TABLE GATE (
                            G_ID VARCHAR(32),
                            AP_ID VARCHAR(32),
                            FOREIGN KEY (AP_ID) REFERENCES AIRPORT(AP_ID) ON DELETE CASCADE ON UPDATE CASCADE,
                            PRIMARY KEY (AP_ID, G_ID)
                            )"""

        create_aircraft_table = """CREATE TABLE AIRCRAFT (
                                AC_ID INT AUTO_INCREMENT,
                                AC_STATUS VARCHAR(32) NOT NULL,
                                AC_MAKE VARCHAR(32) NOT NULL,
                                AC_MILEAGE FLOAT NOT NULL,
                                AC_DATE_CREATED VARCHAR(32) NOT NULL,
                                AC_LAST_MAINTAINED VARCHAR(32),
                                AC_NUM_ECONOMY INT NOT NULL,
                                AC_NUM_BUSINESS INT NOT NULL,
                                AC_NUM_FIRSTCLASS INT NOT NULL,
                                AP_ID VARCHAR(32) NOT NULL,
                                PRIMARY KEY (AC_ID),
                                FOREIGN KEY (AP_ID) REFERENCES AIRPORT(AP_ID) ON DELETE CASCADE ON UPDATE CASCADE
                                )"""

        create_flight_table = """CREATE TABLE FLIGHT (
                                F_ID INT AUTO_INCREMENT,
                                AC_ID INT NOT NULL,
                                F_DISTANCE FLOAT NOT NULL,
                                F_DEPARTURETIME VARCHAR(32) NOT NULL,
                                F_ARRIVALTIME VARCHAR(32) NOT NULL,
                                F_DEPARTUREAIRPORTID VARCHAR(32) NOT NULL,
                                F_ARRIVALAIRPORTID VARCHAR(32) NOT NULL,
                                F_DEPARTUREGATEID VARCHAR(32) NOT NULL,
                                F_ARRIVALGATEID VARCHAR(32) NOT NULL,
                                F_STATUS VARCHAR(32) NOT NULL,
                                PRIMARY KEY (F_ID),
                                CHECK (F_DEPARTUREAIRPORTID <> F_ARRIVALAIRPORTID),
                                FOREIGN KEY (AC_ID) REFERENCES AIRCRAFT(AC_ID),
                                FOREIGN KEY (F_DEPARTUREAIRPORTID, F_DEPARTUREGATEID) REFERENCES GATE(AP_ID, G_ID)
                                ON DELETE CASCADE ON UPDATE CASCADE,
                                FOREIGN KEY (F_ARRIVALAIRPORTID, F_ARRIVALGATEID) REFERENCES GATE(AP_ID, G_ID)
                                ON DELETE CASCADE ON UPDATE CASCADE
                                )"""

        create_employee_table = """CREATE TABLE EMPLOYEE (
                                E_ID INT AUTO_INCREMENT,
                                E_HOURS FLOAT NOT NULL,
                                E_TYPE VARCHAR(32) NOT NULL,
                                E_NAME VARCHAR(32) NOT NULL,
                                E_WAGE FLOAT NOT NULL,
                                PRIMARY KEY (E_ID)
                                )"""

        create_itinerary_table = """CREATE TABLE ITINERARY (
                                I_ID INT AUTO_INCREMENT,
                                I_SEATTYPE VARCHAR(32) NOT NULL,
                                I_SEATCOST FLOAT NOT NULL,
                                I_STATUS VARCHAR(32) NOT NULL,
                                C_ID INT NOT NULL,
                                PRIMARY KEY (I_ID),
                                FOREIGN KEY (C_ID) REFERENCES CUSTOMER(C_ID) ON DELETE CASCADE ON UPDATE CASCADE
                                )"""



        create_baggage_table = """CREATE TABLE BAGGAGE (
                                B_ID INT AUTO_INCREMENT,
                                I_ID INT NOT NULL,
                                B_WEIGHT DECIMAL(5,2) NOT NULL,
                                PRIMARY KEY (B_ID, I_ID),
                                FOREIGN KEY (I_ID) REFERENCES ITINERARY(I_ID) ON DELETE CASCADE ON UPDATE CASCADE
                                )"""

        create_frequentflier_table = """CREATE TABLE FREQUENTFLIER (
                                    C_ID INT,
                                    FF_MILES FLOAT NOT NULL,
                                    PRIMARY KEY (C_ID),
                                    FOREIGN KEY (C_ID) REFERENCES CUSTOMER(C_ID) ON DELETE CASCADE ON UPDATE CASCADE
                                    )"""

        create_workson_table = """CREATE TABLE WORKSON (
                                E_ID INT,
                                F_ID INT,
                                FOREIGN KEY (E_ID) REFERENCES EMPLOYEE(E_ID) ON DELETE CASCADE ON UPDATE CASCADE,
                                FOREIGN KEY (F_ID) REFERENCES FLIGHT(F_ID) ON DELETE CASCADE ON UPDATE CASCADE,
                                PRIMARY KEY (E_ID, F_ID)
                                )"""

        create_schedule_table = """CREATE TABLE SCHEDULE (
                                I_ID INT,
                                F_ID INT,
                                FOREIGN KEY (I_ID) REFERENCES ITINERARY(I_ID) ON DELETE CASCADE ON UPDATE CASCADE,
                                FOREIGN KEY (F_ID) REFERENCES FLIGHT(F_ID) ON DELETE CASCADE ON UPDATE CASCADE,
                                PRIMARY KEY (I_ID, F_ID)
                                )"""

        cursor.execute(create_customer_table)
        print(('Created new {0} table in {1}').format('CUSTOMER',self.db))

        cursor.execute(create_airport_table)
        print(('Created new {0} table in {1}').format('AIRPORT',self.db))

        cursor.execute(create_gate_table)
        print(('Created new {0} table in {1}').format('GATE',self.db))

        cursor.execute(create_aircraft_table)
        print(('Created new {0} table in {1}').format('AIRCRAFT',self.db))

        cursor.execute(create_flight_table)
        print(('Created new {0} table in {1}').format('FLIGHT',self.db))

        cursor.execute(create_employee_table)
        print(('Created new {0} table in {1}').format('EMPLOYEE',self.db))

        cursor.execute(create_itinerary_table)
        print(('Created new {0} table in {1}').format('ITINERARY',self.db))

        cursor.execute(create_baggage_table)
        print(('Created new {0} table in {1}').format('BAGGAGE',self.db))

        cursor.execute(create_frequentflier_table)
        print(('Created new {0} table in {1}').format('FREQUENTFLIER',self.db))

        cursor.execute(create_workson_table)
        print(('Created new {0} table in {1}').format('WORKSON',self.db))

        cursor.execute(create_schedule_table)
        print(('Created new {0} table in {1}').format('SCHEDULE',self.db))

        print(('{0} RESET COMPLETE').format(self.db))
        cursor.close()
        db.close()
        return 0

    '''
    function: populate_db
    description: populate database with test data
    notes: do this right after reset_db()
    '''
    def populate_db(self):
        db = MySQLdb.connect(host=self.host,
                                 user=self.user,
                                 passwd=self.pw,
                                 db=self.db)
        cursor = db.cursor()

        ''' insert test customers'''
        insert_customer_1 = """ INSERT INTO CUSTOMER (C_NAME, C_AGE, C_EMAIL, C_PHONE)
                            VALUES ('Eveline Christa', 20, 'check@test.com', '6041111111')
                            """

        insert_customer_2 = """ INSERT INTO CUSTOMER (C_NAME, C_AGE, C_EMAIL, C_PHONE)
                            VALUES ('Anastasios Cardea', 30, 'check2@test.com', '6042222222')
                            """

        insert_customer_3 = """ INSERT INTO CUSTOMER (C_NAME, C_AGE, C_EMAIL, C_PHONE)
                            VALUES ('Roparzh Theodosios', 40, 'check3@test.com', '6043333333')
                            """

        insert_customer_4 = """ INSERT INTO CUSTOMER (C_NAME, C_AGE, C_EMAIL, C_PHONE)
                            VALUES ('Renate Kamilla', 50, 'check4@test.com', '6044444444')
                            """

        insert_customer_5 = """ INSERT INTO CUSTOMER (C_NAME, C_AGE, C_EMAIL, C_PHONE)
                            VALUES ('Kelleigh Floriano', 55, 'check5@test.com', '6045555555')
                            """

        insert_customer_6 = """ INSERT INTO CUSTOMER (C_NAME, C_AGE, C_EMAIL, C_PHONE)
                            VALUES ('Gyongyi Elvis', 60, 'check6@test.com', '6046666666')
                            """

        insert_customer_7 = """ INSERT INTO CUSTOMER (C_NAME, C_AGE, C_EMAIL, C_PHONE)
                            VALUES ('Prasanna Rachel', 70, 'check7@test.com', '6047777777')
                            """

        insert_customer_8 = """ INSERT INTO CUSTOMER (C_NAME, C_AGE, C_EMAIL, C_PHONE)
                            VALUES ('Adrastea Agamemnon', 73, 'check8@test.com', '6048888888')
                            """

        insert_customer_9 = """ INSERT INTO CUSTOMER (C_NAME, C_AGE, C_EMAIL, C_PHONE)
                            VALUES ('Stephane Freyja', 28, 'check9@test.com', '6049999999')
                            """

        insert_customer_10 = """ INSERT INTO CUSTOMER (C_NAME, C_AGE, C_EMAIL, C_PHONE)
                            VALUES ('Erwin Gaius', 19, 'check10@test.com', '6041010101')
                            """

        try:
            cursor.execute(insert_customer_1)
            cursor.execute(insert_customer_2)
            cursor.execute(insert_customer_3)
            cursor.execute(insert_customer_4)
            cursor.execute(insert_customer_5)
            cursor.execute(insert_customer_6)
            cursor.execute(insert_customer_7)
            cursor.execute(insert_customer_8)
            cursor.execute(insert_customer_9)
            cursor.execute(insert_customer_10)
            db.commit()
        except Exception as e:
            print(e)

        ''' insert test frequentflier '''
        insert_frequentflier_1 = """ INSERT INTO FREQUENTFLIER (C_ID, FF_MILES)
                                 VALUES (1, 200.5)
                                 """
        insert_frequentflier_2 = """ INSERT INTO FREQUENTFLIER (C_ID, FF_MILES)
                                 VALUES (3, 300.5)
                                 """
        insert_frequentflier_3 = """ INSERT INTO FREQUENTFLIER (C_ID, FF_MILES)
                                 VALUES (5, 1920.3)
                                 """
        insert_frequentflier_4 = """ INSERT INTO FREQUENTFLIER (C_ID, FF_MILES)
                                 VALUES (7, 1234.23)
                                 """
        insert_frequentflier_5 = """ INSERT INTO FREQUENTFLIER (C_ID, FF_MILES)
                                 VALUES (8, 5674.23)
                                 """

        try:
            cursor.execute(insert_frequentflier_1)
            cursor.execute(insert_frequentflier_2)
            cursor.execute(insert_frequentflier_3)
            cursor.execute(insert_frequentflier_4)
            cursor.execute(insert_frequentflier_5)
            db.commit()
        except Exception as e:
            print(e)

        ''' insert test airport '''
        insert_airport_1 = """ INSERT INTO AIRPORT (AP_ID, AP_CITY, AP_COUNTRY)
                           VALUES ('YVR', 'VANCOUVER', 'CANADA')
                           """
        insert_airport_2 = """ INSERT INTO AIRPORT (AP_ID, AP_CITY, AP_COUNTRY)
                           VALUES ('JFK', 'NEW YORK', 'USA')
                           """
        insert_airport_3 = """ INSERT INTO AIRPORT (AP_ID, AP_CITY, AP_COUNTRY)
                           VALUES ('LAX', 'LOS ANGELES', 'USA')
                           """
        insert_airport_4 = """ INSERT INTO AIRPORT (AP_ID, AP_CITY, AP_COUNTRY)
                           VALUES ('TPE', 'TAIPEI', 'TAIWAN')
                           """
        insert_airport_5 = """ INSERT INTO AIRPORT (AP_ID, AP_CITY, AP_COUNTRY)
                           VALUES ('YYZ', 'TORONTO', 'CANADA')
                           """
        insert_airport_6 = """ INSERT INTO AIRPORT (AP_ID, AP_CITY, AP_COUNTRY)
                           VALUES ('BOS', 'BOSTON', 'USA')
                           """
        insert_airport_7 = """ INSERT INTO AIRPORT (AP_ID, AP_CITY, AP_COUNTRY)
                           VALUES ('IAH', 'HOUSTON', 'USA')
                           """
        insert_airport_8 = """ INSERT INTO AIRPORT (AP_ID, AP_CITY, AP_COUNTRY)
                           VALUES ('PEK', 'BEIJING', 'CHINA')
                           """
        insert_airport_9 = """ INSERT INTO AIRPORT (AP_ID, AP_CITY, AP_COUNTRY)
                           VALUES ('SHA', 'SHANGHAI', 'CHINA')
                           """
        insert_airport_10 = """ INSERT INTO AIRPORT (AP_ID, AP_CITY, AP_COUNTRY)
                           VALUES ('KIX', 'OSAKA', 'JAPAN')
                           """

        try:
            cursor.execute(insert_airport_1)
            cursor.execute(insert_airport_2)
            cursor.execute(insert_airport_3)
            cursor.execute(insert_airport_4)
            cursor.execute(insert_airport_5)
            cursor.execute(insert_airport_6)
            cursor.execute(insert_airport_7)
            cursor.execute(insert_airport_8)
            cursor.execute(insert_airport_9)
            cursor.execute(insert_airport_10)
            db.commit()
        except Exception as e:
            print(e)


        ''' insert test gate '''
        terminals = ['A', 'B', 'C', 'D', 'E']
        airports = ['YVR', 'JFK', 'LAX', 'TPE', 'YYZ', 'BOS', 'IAH', 'PEK', 'SHA', 'KIX']
        try:
            for airport in airports:
                for t in terminals:
                    for x in range(1, 6):
                        insert_gate = """ INSERT INTO GATE(G_ID, AP_ID)
                                      VALUES('%s', '%s')
                                      """ % (t+str(x), airport)
                        cursor.execute(insert_gate)
            db.commit()
        except Exception as e:
            print(e)

        ''' insert test aircrafts '''
        insert_aircraft_1 = """ INSERT INTO AIRCRAFT (AC_STATUS, AC_MAKE, AC_MILEAGE,
                            AC_DATE_CREATED, AC_LAST_MAINTAINED, AC_NUM_ECONOMY, AC_NUM_BUSINESS,
                            AC_NUM_FIRSTCLASS, AP_ID)
                            VALUES ('IDLE', 'BOEING777-300', 2912374.28, '07-21-1993', '10-25-2017', 300, 100, 15, 'YVR')
                            """
        insert_aircraft_2 = """ INSERT INTO AIRCRAFT (AC_STATUS, AC_MAKE, AC_MILEAGE,
                            AC_DATE_CREATED, AC_LAST_MAINTAINED, AC_NUM_ECONOMY, AC_NUM_BUSINESS,
                            AC_NUM_FIRSTCLASS, AP_ID)
                            VALUES ('INFLIGHT', 'BOEING777-300', 893621.56, '07-21-1993', '10-25-2017', 300, 100, 15, 'KIX')
                            """
        insert_aircraft_3 = """ INSERT INTO AIRCRAFT (AC_STATUS, AC_MAKE, AC_MILEAGE,
                            AC_DATE_CREATED, AC_LAST_MAINTAINED, AC_NUM_ECONOMY, AC_NUM_BUSINESS,
                            AC_NUM_FIRSTCLASS, AP_ID)
                            VALUES ('IDLE', 'BOEING777-300', 1238650.82, '07-21-1993', '10-25-2017', 300, 100, 15, 'BOS')
                            """


        insert_aircraft_4 = """ INSERT INTO AIRCRAFT (AC_STATUS, AC_MAKE, AC_MILEAGE,
                            AC_DATE_CREATED, AC_LAST_MAINTAINED, AC_NUM_ECONOMY, AC_NUM_BUSINESS,
                            AC_NUM_FIRSTCLASS, AP_ID)
                            VALUES ('IDLE', 'BOEING787-10', 972172.53, '12-25-2005', '10-03-2017', 350, 100, 30, 'TPE')
                            """
        insert_aircraft_5 = """ INSERT INTO AIRCRAFT (AC_STATUS, AC_MAKE, AC_MILEAGE,
                            AC_DATE_CREATED, AC_LAST_MAINTAINED, AC_NUM_ECONOMY, AC_NUM_BUSINESS,
                            AC_NUM_FIRSTCLASS, AP_ID)
                            VALUES ('INFLIGHT', 'BOEING787-10', 432642.36, '12-25-2005', '10-03-2017', 350, 100, 30, 'SHA')
                            """
        insert_aircraft_6 = """ INSERT INTO AIRCRAFT (AC_STATUS, AC_MAKE, AC_MILEAGE,
                            AC_DATE_CREATED, AC_LAST_MAINTAINED, AC_NUM_ECONOMY, AC_NUM_BUSINESS,
                            AC_NUM_FIRSTCLASS, AP_ID)
                            VALUES ('INFLIGHT', 'BOEING787-10', 261347.09, '12-25-2005', '10-03-2017', 350, 100, 30, 'PEK')
                            """

        insert_aircraft_7 = """ INSERT INTO AIRCRAFT (AC_STATUS, AC_MAKE, AC_MILEAGE,
                            AC_DATE_CREATED, AC_LAST_MAINTAINED, AC_NUM_ECONOMY, AC_NUM_BUSINESS,
                            AC_NUM_FIRSTCLASS, AP_ID)
                            VALUES ('IDLE', 'AIRBUS A330-300', 146754.43, '11-18-1994', '11-03-2017', 100, 50, 15, 'JFK')
                            """

        insert_aircraft_8 = """ INSERT INTO AIRCRAFT (AC_STATUS, AC_MAKE, AC_MILEAGE,
                            AC_DATE_CREATED, AC_LAST_MAINTAINED, AC_NUM_ECONOMY, AC_NUM_BUSINESS,
                            AC_NUM_FIRSTCLASS, AP_ID)
                            VALUES ('INFLIGHT', 'AIRBUS A330-300', 234752.95, '11-18-1994', '11-03-2017', 100, 50, 15, 'LAX')
                            """
        insert_aircraft_9 = """ INSERT INTO AIRCRAFT (AC_STATUS, AC_MAKE, AC_MILEAGE,
                            AC_DATE_CREATED, AC_LAST_MAINTAINED, AC_NUM_ECONOMY, AC_NUM_BUSINESS,
                            AC_NUM_FIRSTCLASS, AP_ID)
                            VALUES ('IDLE', 'AIRBUS A330-300', 16532435.23, '11-18-1994', '11-03-2017', 100, 50, 15, 'LAX')
                            """
        insert_aircraft_10 = """ INSERT INTO AIRCRAFT (AC_STATUS, AC_MAKE, AC_MILEAGE,
                            AC_DATE_CREATED, AC_LAST_MAINTAINED, AC_NUM_ECONOMY, AC_NUM_BUSINESS,
                            AC_NUM_FIRSTCLASS, AP_ID)
                            VALUES ('INFLIGHT', 'AIRBUS A330-300', 34754323.12, '11-18-1994', '11-03-2017', 100, 50, 15, 'LAX')
                            """

        try:
            cursor.execute(insert_aircraft_1)
            cursor.execute(insert_aircraft_2)
            cursor.execute(insert_aircraft_3)
            cursor.execute(insert_aircraft_4)
            cursor.execute(insert_aircraft_5)
            cursor.execute(insert_aircraft_6)
            cursor.execute(insert_aircraft_7)
            cursor.execute(insert_aircraft_8)
            cursor.execute(insert_aircraft_9)
            cursor.execute(insert_aircraft_10)
            db.commit()
        except Exception as e:
            print(e)

        ''' insert test flights '''
        insert_flight_1 = """ INSERT INTO FLIGHT (AC_ID, F_DISTANCE,
                            F_DEPARTURETIME, F_ARRIVALTIME, F_DEPARTUREAIRPORTID, F_ARRIVALAIRPORTID,
                            F_DEPARTUREGATEID, F_ARRIVALGATEID, F_STATUS)
                            VALUES (1, 5000, '01-10-2018:23:23', '01-12-2018:06:23', 'YVR', 'TPE', 'A1', 'E5', 'ONTIME')
                            """
        insert_flight_2 = """ INSERT INTO FLIGHT (AC_ID, F_DISTANCE,
                            F_DEPARTURETIME, F_ARRIVALTIME, F_DEPARTUREAIRPORTID, F_ARRIVALAIRPORTID,
                            F_DEPARTUREGATEID, F_ARRIVALGATEID, F_STATUS)
                            VALUES (3, 250, '01-08-2018:05:23', '01-08-2018:06:23', 'LAX', 'YVR', 'C5', 'B3', 'ONTIME')
                            """

        insert_flight_3 = """ INSERT INTO FLIGHT (AC_ID, F_DISTANCE,
                            F_DEPARTURETIME, F_ARRIVALTIME, F_DEPARTUREAIRPORTID, F_ARRIVALAIRPORTID,
                            F_DEPARTUREGATEID, F_ARRIVALGATEID, F_STATUS)
                            VALUES (2, 4500, '01-13-2018:05:23', '01-13-2018:17:23', 'TPE', 'JFK', 'E2', 'A3', 'ONTIME')
                            """
        insert_flight_4 = """ INSERT INTO FLIGHT (AC_ID, F_DISTANCE,
                            F_DEPARTURETIME, F_ARRIVALTIME, F_DEPARTUREAIRPORTID, F_ARRIVALAIRPORTID,
                            F_DEPARTUREGATEID, F_ARRIVALGATEID, F_STATUS)
                            VALUES (4, 1423, '01-21-2018:05:23', '01-21-2018:17:23', 'BOS', 'IAH', 'C2', 'E3', 'ONTIME')
                            """
        insert_flight_5 = """ INSERT INTO FLIGHT (AC_ID, F_DISTANCE,
                            F_DEPARTURETIME, F_ARRIVALTIME, F_DEPARTUREAIRPORTID, F_ARRIVALAIRPORTID,
                            F_DEPARTUREGATEID, F_ARRIVALGATEID, F_STATUS)
                            VALUES (5, 2345, '01-24-2018:05:23', '01-25-2018:17:23', 'LAX', 'PEK', 'D2', 'A1', 'DELAYED')
                            """
        insert_flight_6 = """ INSERT INTO FLIGHT (AC_ID, F_DISTANCE,
                            F_DEPARTURETIME, F_ARRIVALTIME, F_DEPARTUREAIRPORTID, F_ARRIVALAIRPORTID,
                            F_DEPARTUREGATEID, F_ARRIVALGATEID, F_STATUS)
                            VALUES (6, 8102, '01-09-2018:05:23', '01-10-2018:17:23', 'SHA', 'BOS', 'B2', 'A5', 'DELAYED')
                            """
        insert_flight_7 = """ INSERT INTO FLIGHT (AC_ID, F_DISTANCE,
                            F_DEPARTURETIME, F_ARRIVALTIME, F_DEPARTUREAIRPORTID, F_ARRIVALAIRPORTID,
                            F_DEPARTUREGATEID, F_ARRIVALGATEID, F_STATUS)
                            VALUES (7, 940, '01-01-2018:05:23', '01-02-2018:17:23', 'KIX', 'IAH', 'B4', 'D2', 'DELAYED')
                            """
        insert_flight_8 = """ INSERT INTO FLIGHT (AC_ID, F_DISTANCE,
                            F_DEPARTURETIME, F_ARRIVALTIME, F_DEPARTUREAIRPORTID, F_ARRIVALAIRPORTID,
                            F_DEPARTUREGATEID, F_ARRIVALGATEID, F_STATUS)
                            VALUES (8, 9402, '01-06-2018:05:23', '01-07-2018:17:23', 'TPE', 'YYZ', 'E4', 'E3', 'DELAYED')
                            """
        insert_flight_9 = """ INSERT INTO FLIGHT (AC_ID, F_DISTANCE,
                            F_DEPARTURETIME, F_ARRIVALTIME, F_DEPARTUREAIRPORTID, F_ARRIVALAIRPORTID,
                            F_DEPARTUREGATEID, F_ARRIVALGATEID, F_STATUS)
                            VALUES (9, 9302, '01-08-2018:05:23', '01-08-2018:17:23', 'YYZ', 'BOS', 'A2', 'A3', 'CANCELED')
                            """
        insert_flight_10 = """ INSERT INTO FLIGHT (AC_ID, F_DISTANCE,
                            F_DEPARTURETIME, F_ARRIVALTIME, F_DEPARTUREAIRPORTID, F_ARRIVALAIRPORTID,
                            F_DEPARTUREGATEID, F_ARRIVALGATEID, F_STATUS)
                            VALUES (10, 7123, '01-13-2018:05:23', '01-13-2018:17:23', 'SHA', 'LAX', 'B2', 'C2', 'CANCELED')
                            """


        try:
            cursor.execute(insert_flight_1)
            cursor.execute(insert_flight_2)
            cursor.execute(insert_flight_3)
            cursor.execute(insert_flight_4)
            cursor.execute(insert_flight_5)
            cursor.execute(insert_flight_6)
            cursor.execute(insert_flight_7)
            cursor.execute(insert_flight_8)
            cursor.execute(insert_flight_9)
            cursor.execute(insert_flight_10)
            db.commit()
        except Exception as e:
            print(e)

        ''' insert test employees '''
        insert_employee_1 = """ INSERT INTO EMPLOYEE (E_HOURS, E_TYPE, E_NAME, E_WAGE)
                            VALUES (70.2, "CAPTAIN", "Heino Amir", 53)
                            """
        insert_employee_2 = """ INSERT INTO EMPLOYEE (E_HOURS, E_TYPE, E_NAME, E_WAGE)
                            VALUES (86.3, "CAPTAIN", "Caleb Priska", 63)
                            """
        insert_employee_3 = """ INSERT INTO EMPLOYEE (E_HOURS, E_TYPE, E_NAME, E_WAGE)
                            VALUES (92, "CAPTAIN", "Ralf Jordana", 80)
                            """
        insert_employee_4 = """ INSERT INTO EMPLOYEE (E_HOURS, E_TYPE, E_NAME, E_WAGE)
                            VALUES (41.4, "CAPTAIN", "Bahadur Lyubov", 90)
                            """
        insert_employee_5 = """ INSERT INTO EMPLOYEE (E_HOURS, E_TYPE, E_NAME, E_WAGE)
                            VALUES (00, "CAPTAIN", "Gervasio Qasim", 105)
                            """

        insert_employee_6 = """ INSERT INTO EMPLOYEE (E_HOURS, E_TYPE, E_NAME, E_WAGE)
                            VALUES (90.5, "ATTENDANT", "Mahalia Reka", 35)
                            """
        insert_employee_7 = """ INSERT INTO EMPLOYEE (E_HOURS, E_TYPE, E_NAME, E_WAGE)
                            VALUES (124.3, "ATTENDANT", "Klara Maire", 36)
                            """
        insert_employee_8 = """ INSERT INTO EMPLOYEE (E_HOURS, E_TYPE, E_NAME, E_WAGE)
                            VALUES (89.4, "ATTENDANT", "Gwallter Elaine", 30)
                            """
        insert_employee_9 = """ INSERT INTO EMPLOYEE (E_HOURS, E_TYPE, E_NAME, E_WAGE)
                            VALUES (109.0, "ATTENDANT", "Eluned Helge", 29)
                            """
        insert_employee_10 = """ INSERT INTO EMPLOYEE (E_HOURS, E_TYPE, E_NAME, E_WAGE)
                            VALUES (84.2, "ATTENDANT", "Tamara Shantanu", 38)
                            """
        try:
            cursor.execute(insert_employee_1)
            cursor.execute(insert_employee_2)
            cursor.execute(insert_employee_3)
            cursor.execute(insert_employee_4)
            cursor.execute(insert_employee_5)
            cursor.execute(insert_employee_6)
            cursor.execute(insert_employee_7)
            cursor.execute(insert_employee_8)
            cursor.execute(insert_employee_9)
            cursor.execute(insert_employee_10)
            db.commit()
        except Exception as e:
            print(e)

        ''' insert test itinerary '''
        insert_itinerary_1 = """ INSERT INTO ITINERARY(I_SEATTYPE, I_SEATCOST, I_STATUS, C_ID)
                             VALUES ('FIRSTCLASS', 53.5, 'PAID', 1)
                             """
        insert_itinerary_2 = """ INSERT INTO ITINERARY(I_SEATTYPE, I_SEATCOST, I_STATUS, C_ID)
                             VALUES ('BUSINESS', 24.7, 'CHECKEDIN', 2)
                             """
        insert_itinerary_3 = """ INSERT INTO ITINERARY(I_SEATTYPE, I_SEATCOST, I_STATUS, C_ID)
                             VALUES ('ECONOMY', 3.5, 'DONE', 3)
                             """
        insert_itinerary_4 = """ INSERT INTO ITINERARY(I_SEATTYPE, I_SEATCOST, I_STATUS, C_ID)
                             VALUES ('FIRSTCLASS', 50.3, 'CANCELED', 4)
                             """
        insert_itinerary_5 = """ INSERT INTO ITINERARY(I_SEATTYPE, I_SEATCOST, I_STATUS, C_ID)
                             VALUES ('FIRSTCLASS', 54.2, 'PAID', 5)
                             """
        insert_itinerary_6 = """ INSERT INTO ITINERARY(I_SEATTYPE, I_SEATCOST, I_STATUS, C_ID)
                             VALUES ('BUSINESS', 24.2, 'CHECKEDIN', 6)
                             """
        insert_itinerary_7 = """ INSERT INTO ITINERARY(I_SEATTYPE, I_SEATCOST, I_STATUS, C_ID)
                             VALUES ('ECONOMY', 2.5, 'DONE', 7)
                             """
        insert_itinerary_8 = """ INSERT INTO ITINERARY(I_SEATTYPE, I_SEATCOST, I_STATUS, C_ID)
                             VALUES ('ECONOMY', 2.3, 'CANCELED', 8)
                             """
        insert_itinerary_9 = """ INSERT INTO ITINERARY(I_SEATTYPE, I_SEATCOST, I_STATUS, C_ID)
                             VALUES ('ECONOMY', 4.4, 'PAID', 9)
                             """
        insert_itinerary_10 = """ INSERT INTO ITINERARY(I_SEATTYPE, I_SEATCOST, I_STATUS, C_ID)
                             VALUES ('ECONOMY', 7.3, 'DONE', 10)
                             """
        insert_itinerary_11 = """ INSERT INTO ITINERARY(I_SEATTYPE, I_SEATCOST, I_STATUS, C_ID)
                             VALUES ('BUSINESS', 24.7, 'CHECKEDIN', 1)
                             """
        insert_itinerary_12 = """ INSERT INTO ITINERARY(I_SEATTYPE, I_SEATCOST, I_STATUS, C_ID)
                             VALUES ('ECONOMY', 3.5, 'DONE', 1)
                             """
        insert_itinerary_13 = """ INSERT INTO ITINERARY(I_SEATTYPE, I_SEATCOST, I_STATUS, C_ID)
                             VALUES ('FIRSTCLASS', 50.3, 'CANCELED', 1)
                             """
        insert_itinerary_14 = """ INSERT INTO ITINERARY(I_SEATTYPE, I_SEATCOST, I_STATUS, C_ID)
                             VALUES ('FIRSTCLASS', 54.2, 'PAID', 1)
                             """
        insert_itinerary_15 = """ INSERT INTO ITINERARY(I_SEATTYPE, I_SEATCOST, I_STATUS, C_ID)
                             VALUES ('BUSINESS', 24.2, 'PAID', 1)
                             """
        insert_itinerary_16 = """ INSERT INTO ITINERARY(I_SEATTYPE, I_SEATCOST, I_STATUS, C_ID)
                             VALUES ('ECONOMY', 2.5, 'DONE', 1)
                             """
        insert_itinerary_17 = """ INSERT INTO ITINERARY(I_SEATTYPE, I_SEATCOST, I_STATUS, C_ID)
                             VALUES ('ECONOMY', 2.3, 'CANCELED', 1)
                             """
        insert_itinerary_18 = """ INSERT INTO ITINERARY(I_SEATTYPE, I_SEATCOST, I_STATUS, C_ID)
                             VALUES ('ECONOMY', 4.4, 'PAID', 1)
                             """
        insert_itinerary_19 = """ INSERT INTO ITINERARY(I_SEATTYPE, I_SEATCOST, I_STATUS, C_ID)
                             VALUES ('ECONOMY', 7.3, 'DONE', 1)
                             """


        try:
            cursor.execute(insert_itinerary_1)
            cursor.execute(insert_itinerary_2)
            cursor.execute(insert_itinerary_3)
            cursor.execute(insert_itinerary_4)
            cursor.execute(insert_itinerary_5)
            cursor.execute(insert_itinerary_6)
            cursor.execute(insert_itinerary_7)
            cursor.execute(insert_itinerary_8)
            cursor.execute(insert_itinerary_9)
            cursor.execute(insert_itinerary_10)
            cursor.execute(insert_itinerary_11)
            cursor.execute(insert_itinerary_12)
            cursor.execute(insert_itinerary_13)
            cursor.execute(insert_itinerary_14)
            cursor.execute(insert_itinerary_15)
            cursor.execute(insert_itinerary_16)
            cursor.execute(insert_itinerary_17)
            cursor.execute(insert_itinerary_18)
            cursor.execute(insert_itinerary_19)
            db.commit()
        except Exception as e:
            print(e)

        ''' insert test baggage '''
        insert_baggage_1 = """ INSERT INTO BAGGAGE (I_ID, B_WEIGHT)
                           VALUES (1, 89.78)
                           """
        insert_baggage_2 = """ INSERT INTO BAGGAGE (I_ID, B_WEIGHT)
                           VALUES (1, 95.96)
                           """
        insert_baggage_3 = """ INSERT INTO BAGGAGE (I_ID, B_WEIGHT)
                           VALUES (2, 84.67)
                           """
        insert_baggage_4 = """ INSERT INTO BAGGAGE (I_ID, B_WEIGHT)
                           VALUES (2, 125.67)
                           """
        insert_baggage_5 = """ INSERT INTO BAGGAGE (I_ID, B_WEIGHT)
                           VALUES (3, 70.44)
                           """
        insert_baggage_6 = """ INSERT INTO BAGGAGE (I_ID, B_WEIGHT)
                           VALUES (5, 88.75)
                           """
        insert_baggage_7 = """ INSERT INTO BAGGAGE (I_ID, B_WEIGHT)
                           VALUES (7, 55.85)
                           """
        insert_baggage_8 = """ INSERT INTO BAGGAGE (I_ID, B_WEIGHT)
                           VALUES (7, 122.94)
                           """
        insert_baggage_9 = """ INSERT INTO BAGGAGE (I_ID, B_WEIGHT)
                           VALUES (9, 25.23)
                           """
        insert_baggage_10 = """ INSERT INTO BAGGAGE (I_ID, B_WEIGHT)
                           VALUES (10, 93.47)
                           """

        try:
            cursor.execute(insert_baggage_1)
            cursor.execute(insert_baggage_2)
            cursor.execute(insert_baggage_3)
            cursor.execute(insert_baggage_4)
            cursor.execute(insert_baggage_5)
            cursor.execute(insert_baggage_6)
            cursor.execute(insert_baggage_7)
            cursor.execute(insert_baggage_8)
            cursor.execute(insert_baggage_9)
            cursor.execute(insert_baggage_10)
            db.commit()
        except Exception as e:
            print(e)

        ''' insert test workon '''
        insert_workon_1 = """ INSERT INTO WORKSON(E_ID, F_ID)
                             VALUES (1, 1)
                             """
        insert_workon_2 = """ INSERT INTO WORKSON(E_ID, F_ID)
                             VALUES (6, 1)
                             """
        insert_workon_3 = """ INSERT INTO WORKSON(E_ID, F_ID)
                             VALUES (7, 1)
                             """
        insert_workon_4 = """ INSERT INTO WORKSON(E_ID, F_ID)
                             VALUES (8, 1)
                             """
        insert_workon_5 = """ INSERT INTO WORKSON(E_ID, F_ID)
                             VALUES (9, 1)
                             """
        insert_workon_6 = """ INSERT INTO WORKSON(E_ID, F_ID)
                             VALUES (10, 1)
                             """
        insert_workon_7 = """ INSERT INTO WORKSON(E_ID, F_ID)
                             VALUES (3, 2)
                             """
        insert_workon_8 = """ INSERT INTO WORKSON(E_ID, F_ID)
                             VALUES (5, 2)
                             """
        insert_workon_9 = """ INSERT INTO WORKSON(E_ID, F_ID)
                             VALUES (6, 2)
                             """
        insert_workon_10 = """ INSERT INTO WORKSON(E_ID, F_ID)
                             VALUES (7, 2)
                             """
        insert_workon_11 = """ INSERT INTO WORKSON(E_ID, F_ID)
                             VALUES (8, 2)
                             """
        insert_workon_12 = """ INSERT INTO WORKSON(E_ID, F_ID)
                             VALUES (9, 2)
                             """
        insert_workon_13 = """ INSERT INTO WORKSON(E_ID, F_ID)
                             VALUES (2, 3)
                             """
        insert_workon_14 = """ INSERT INTO WORKSON(E_ID, F_ID)
                             VALUES (4, 3)
                             """
        insert_workon_15 = """ INSERT INTO WORKSON(E_ID, F_ID)
                             VALUES (7, 3)
                             """
        insert_workon_16 = """ INSERT INTO WORKSON(E_ID, F_ID)
                             VALUES (9, 3)
                             """
        insert_workon_17 = """ INSERT INTO WORKSON(E_ID, F_ID)
                             VALUES (10, 3)
                             """
        insert_workon_18 = """ INSERT INTO WORKSON(E_ID, F_ID)
                             VALUES (3, 4)
                             """
        insert_workon_19 = """ INSERT INTO WORKSON(E_ID, F_ID)
                             VALUES (5, 4)
                             """
        insert_workon_20 = """ INSERT INTO WORKSON(E_ID, F_ID)
                             VALUES (6, 4)
                             """
        insert_workon_21 = """ INSERT INTO WORKSON(E_ID, F_ID)
                             VALUES (7, 4)
                             """
        insert_workon_22 = """ INSERT INTO WORKSON(E_ID, F_ID)
                             VALUES (8, 4)
                             """
        insert_workon_23 = """ INSERT INTO WORKSON(E_ID, F_ID)
                             VALUES (9, 4)
                             """
        insert_workon_24 = """ INSERT INTO WORKSON(E_ID, F_ID)
                             VALUES (1, 5)
                             """
        insert_workon_25 = """ INSERT INTO WORKSON(E_ID, F_ID)
                             VALUES (5, 5)
                             """
        insert_workon_26 = """ INSERT INTO WORKSON(E_ID, F_ID)
                             VALUES (7, 5)
                             """
        insert_workon_27 = """ INSERT INTO WORKSON(E_ID, F_ID)
                             VALUES (9, 5)
                             """
        insert_workon_28 = """ INSERT INTO WORKSON(E_ID, F_ID)
                             VALUES (6, 5)
                             """
        insert_workon_29 = """ INSERT INTO WORKSON(E_ID, F_ID)
                             VALUES (10, 5)
                             """
        insert_workon_30 = """ INSERT INTO WORKSON(E_ID, F_ID)
                             VALUES (3, 6)
                             """
        insert_workon_31 = """ INSERT INTO WORKSON(E_ID, F_ID)
                             VALUES (1, 6)
                             """
        insert_workon_32 = """ INSERT INTO WORKSON(E_ID, F_ID)
                             VALUES (6, 6)
                             """
        insert_workon_33 = """ INSERT INTO WORKSON(E_ID, F_ID)
                             VALUES (7, 6)
                             """
        insert_workon_34 = """ INSERT INTO WORKSON(E_ID, F_ID)
                             VALUES (9, 6)
                             """
        insert_workon_35 = """ INSERT INTO WORKSON(E_ID, F_ID)
                             VALUES (10, 6)
                             """
        insert_workon_36 = """ INSERT INTO WORKSON(E_ID, F_ID)
                             VALUES (4, 7)
                             """
        insert_workon_37 = """ INSERT INTO WORKSON(E_ID, F_ID)
                             VALUES (7, 7)
                             """
        insert_workon_38 = """ INSERT INTO WORKSON(E_ID, F_ID)
                             VALUES (8, 7)
                             """
        insert_workon_39 = """ INSERT INTO WORKSON(E_ID, F_ID)
                             VALUES (9, 7)
                             """
        insert_workon_40 = """ INSERT INTO WORKSON(E_ID, F_ID)
                             VALUES (10, 7)
                             """
        insert_workon_41 = """ INSERT INTO WORKSON(E_ID, F_ID)
                             VALUES (4, 8)
                             """
        insert_workon_42 = """ INSERT INTO WORKSON(E_ID, F_ID)
                             VALUES (7, 8)
                             """
        insert_workon_43 = """ INSERT INTO WORKSON(E_ID, F_ID)
                             VALUES (6, 8)
                             """
        insert_workon_44 = """ INSERT INTO WORKSON(E_ID, F_ID)
                             VALUES (8, 8)
                             """
        insert_workon_45 = """ INSERT INTO WORKSON(E_ID, F_ID)
                             VALUES (10, 8)
                             """

        try:
            cursor.execute(insert_workon_1)
            cursor.execute(insert_workon_2)
            cursor.execute(insert_workon_3)
            cursor.execute(insert_workon_4)
            cursor.execute(insert_workon_5)
            cursor.execute(insert_workon_6)
            cursor.execute(insert_workon_7)
            cursor.execute(insert_workon_8)
            cursor.execute(insert_workon_9)
            cursor.execute(insert_workon_10)
            cursor.execute(insert_workon_11)
            cursor.execute(insert_workon_12)
            cursor.execute(insert_workon_13)
            cursor.execute(insert_workon_14)
            cursor.execute(insert_workon_15)
            cursor.execute(insert_workon_16)
            cursor.execute(insert_workon_17)
            cursor.execute(insert_workon_18)
            cursor.execute(insert_workon_19)
            cursor.execute(insert_workon_20)
            cursor.execute(insert_workon_21)
            cursor.execute(insert_workon_22)
            cursor.execute(insert_workon_23)
            cursor.execute(insert_workon_24)
            cursor.execute(insert_workon_25)
            cursor.execute(insert_workon_26)
            cursor.execute(insert_workon_27)
            cursor.execute(insert_workon_28)
            cursor.execute(insert_workon_29)
            cursor.execute(insert_workon_30)
            cursor.execute(insert_workon_31)
            cursor.execute(insert_workon_32)
            cursor.execute(insert_workon_33)
            cursor.execute(insert_workon_34)
            cursor.execute(insert_workon_35)
            cursor.execute(insert_workon_36)
            cursor.execute(insert_workon_37)
            cursor.execute(insert_workon_38)
            cursor.execute(insert_workon_39)
            cursor.execute(insert_workon_40)
            cursor.execute(insert_workon_41)
            cursor.execute(insert_workon_42)
            cursor.execute(insert_workon_43)
            cursor.execute(insert_workon_44)
            cursor.execute(insert_workon_45)
            print(('populated WORKSON table'))
            db.commit()
        except Exception as e:
            print(e)

        ''' insert test schedule '''
        insert_schedule_1 = """ INSERT INTO SCHEDULE(I_ID, F_ID)
                            VALUES (1, 2)
                            """
        insert_schedule_2 = """ INSERT INTO SCHEDULE(I_ID, F_ID)
                            VALUES (1, 1)
                            """
        insert_schedule_3 = """ INSERT INTO SCHEDULE(I_ID, F_ID)
                            VALUES (2, 3)
                            """
        insert_schedule_4 = """ INSERT INTO SCHEDULE(I_ID, F_ID)
                            VALUES (2, 4)
                            """
        insert_schedule_5 = """ INSERT INTO SCHEDULE(I_ID, F_ID)
                            VALUES (2, 5)
                            """
        insert_schedule_6 = """ INSERT INTO SCHEDULE(I_ID, F_ID)
                            VALUES (5, 3)
                            """
        insert_schedule_7 = """ INSERT INTO SCHEDULE(I_ID, F_ID)
                            VALUES (6, 8)
                            """
        insert_schedule_8 = """ INSERT INTO SCHEDULE(I_ID, F_ID)
                            VALUES (9, 6)
                            """
        insert_schedule_9 = """ INSERT INTO SCHEDULE(I_ID, F_ID)
                            VALUES (9, 7)
                            """
        insert_schedule_10 = """ INSERT INTO SCHEDULE(I_ID, F_ID)
                            VALUES (11, 3)
                            """
        insert_schedule_11 = """ INSERT INTO SCHEDULE(I_ID, F_ID)
                            VALUES (11, 4)
                            """
        insert_schedule_12 = """ INSERT INTO SCHEDULE(I_ID, F_ID)
                            VALUES (11, 5)
                            """
        insert_schedule_13 = """ INSERT INTO SCHEDULE(I_ID, F_ID)
                            VALUES (14, 3)
                            """
        insert_schedule_14 = """ INSERT INTO SCHEDULE(I_ID, F_ID)
                            VALUES (15, 8)
                            """
        insert_schedule_15 = """ INSERT INTO SCHEDULE(I_ID, F_ID)
                            VALUES (18, 6)
                            """
        insert_schedule_16 = """ INSERT INTO SCHEDULE(I_ID, F_ID)
                            VALUES (18, 7)
                            """

        try:
            cursor.execute(insert_schedule_1)
            cursor.execute(insert_schedule_2)
            cursor.execute(insert_schedule_3)
            cursor.execute(insert_schedule_4)
            cursor.execute(insert_schedule_5)
            cursor.execute(insert_schedule_6)
            cursor.execute(insert_schedule_7)
            cursor.execute(insert_schedule_8)
            cursor.execute(insert_schedule_9)
            cursor.execute(insert_schedule_10)
            cursor.execute(insert_schedule_11)
            cursor.execute(insert_schedule_12)
            cursor.execute(insert_schedule_13)
            cursor.execute(insert_schedule_14)
            cursor.execute(insert_schedule_15)
            cursor.execute(insert_schedule_16)
            print(('populated schedule table'))
            db.commit()
        except Exception as e:
            print(e)
            db.rollback()

        ''' CREATE VIEWS '''
        create_vip_view = """ CREATE OR REPLACE VIEW VIP AS
                          SELECT DISTINCT C.C_ID, C_NAME, C_AGE, C_EMAIL, C_PHONE
                          FROM CUSTOMER C, ITINERARY I
                          WHERE C.C_ID = I.C_ID AND I.I_SEATTYPE = 'FIRSTCLASS'"""

        create_delayed_flight_view = """ CREATE OR REPLACE VIEW DELAYED_FLIGHT AS
                                     SELECT * FROM FLIGHT
                                     WHERE F_STATUS = 'DELAYED'"""
        try:
            cursor.execute(create_vip_view)
            cursor.execute(create_delayed_flight_view)
            db.commit()
        except Exception as e:
            print(e)
            db.rollback()

        print(('{0} POPULATE COMPLETE').format(self.db))
        cursor.close()
        db.close()
        return 0

#==============================================================================
#   function: add_baggage
#   description: add baggage instance for cust_id
#   return: baggage json object
#==============================================================================

    def add_baggage(self, itinerary_id, bag_weight):
        db = MySQLdb.connect(host=self.host,
                             user=self.user,
                             passwd=self.pw,
                             db=self.db)
        add_baggage_query = """INSERT INTO BAGGAGE(I_ID, B_WEIGHT)
                                VALUES(%s, %.2f)""" % (itinerary_id, float(bag_weight))

        cursor = db.cursor()
        try:
            cursor.execute(add_baggage_query)
            db.commit()
            bag_object = {
                    'bag_id': cursor.lastrowid,
                    'itinerary_id': itinerary_id,
                    'weight': bag_weight
                }
            data = json.dumps(bag_object, sort_keys=True, indent=4, separators=(',', ': '))
        except Exception as e:
            print("Add Baggage Failed with error: {0}".format(e))
            db.rollback()
            data = 0

        cursor.close()
        db.close()
        return data

#==============================================================================
#   function: get_baggage
#   description: returns an instance of baggage based on itinerary ID
#   return: baggage json object
#==============================================================================
    def get_baggage(self, i_id):
        db = MySQLdb.connect(host=self.host,
                             user=self.user,
                             passwd=self.pw,
                             db=self.db)
        if i_id is None:
            get_baggage_query = """SELECT * FROM BAGGAGE"""
        else:
            get_baggage_query = """SELECT * FROM BAGGAGE WHERE I_ID = %d""" % int(i_id)
        cursor = db.cursor()
        try:
            dataList = []
            cursor.execute(get_baggage_query)
            if i_id is None:
                baggage = cursor.fetchall()
                for bag in baggage:
                    bag_object = {
                        'bag_id': bag[0],
                        'itinerary_id': bag[1],
                        'weight': str(bag[2])
                    }
                    dataList.append(bag_object)
            else:
                baggage = cursor.fetchall()
                for bag in baggage:
                    bag_object = {
                        'bag_id': bag[0],
                        'itinerary_id': bag[1],
                        'weight': str(bag[2])
                    }
                    dataList.append(bag_object)
            data = json.dumps(dataList, sort_keys=True, indent=4, separators=(',', ': '))
        except Exception as e:
            print("Get Baggage Failed with error: {0}".format(e))
            db.rollback()
            data = 0

        cursor.close()
        db.close()
        return data

#==============================================================================
#   function: get_baggage for flight
#   description: returns all baggage on flight id
#   return: baggage json object
#==============================================================================
    def get_baggage_for_flight(self, flight_id):
        db = MySQLdb.connect(host=self.host,
                             user=self.user,
                             passwd=self.pw,
                             db=self.db)
        get_baggage_query = """ Select I.I_ID, B.B_ID, S.F_ID from ITINERARY I, SCHEDULE S, BAGGAGE B
                                where B.I_ID = I.I_ID and S.I_ID = I.I_ID and S.F_ID = %d """ % int(flight_id)
        cursor=db.cursor()
        try:
            dataList = []
            cursor.execute(get_baggage_query)
            print("query executed")
            baggage = cursor.fetchall()
            for bag in baggage:
                bag_object = {
                    'bag_id': bag[0],
                    'itinerary_id': bag[1],
                    'weight': str(bag[2])
                }
                dataList.append(bag_object)
            data = json.dumps(dataList, sort_keys=True, indent=4, separators=(',', ': '))
        except Exception as e:
            print("Get Baggage Failed with error: {0}".format(e))
            db.rollback()
            data = 0

        cursor.close()
        db.close()
        return data

#==============================================================================
#   function: delete_baggage
#   description: deletes baggage
#   return: nothing
#==============================================================================
    def delete_baggage(self, b_id):
        db = MySQLdb.connect(host=self.host,
                             user=self.user,
                             passwd=self.pw,
                             db=self.db)
        delete_baggage_query = """DELETE FROM BAGGAGE WHERE B_ID = %d""" % int(b_id)
        cursor = db.cursor()
        deleted_baggage = {
            'baggage_id' : int(b_id)
        }
        try:
            cursor.execute(delete_baggage_query)
            db.commit()
            data = json.dumps(deleted_baggage, sort_keys=True, indent=4, separators=(',', ': '))
        except Exception as e:
            print("Delete Baggage Failed with error: {0}".format(e))
            db.rollback()
            data = 0

        cursor.close()
        db.close()
        return data

#==============================================================================
#   function: get_customer
#   description: returns an instance of customer based on customer_id
#   return: customer json object
#==============================================================================
    def get_customer(self, customer_id):
        db = MySQLdb.connect(host=self.host,
                             user=self.user,
                             passwd=self.pw,
                             db=self.db)
        if (customer_id==None):
            get_customer_query = """SELECT * FROM CUSTOMER"""
        else:
            get_customer_query = """SELECT * FROM CUSTOMER
                                WHERE C_ID = %d""" % int(customer_id)
        cursor = db.cursor()
        try:
            dataList = []
            cursor.execute(get_customer_query)
            if customer_id is None:
                customers = cursor.fetchall()
                for c in customers:
                    c_object = {
                        'customer_id': c[0],
                        'customer_name': c[1],
                        'customer_age': c[2],
                        'customer_email': c[3],
                        'customer_phone': c[4]
                    }
                    dataList.append(c_object)
            else:
                customers = cursor.fetchone()
                c_object = {
                    'customer_id': customers[0],
                    'customer_name': customers[1],
                    'customer_age': customers[2],
                    'customer_email': customers[3],
                    'customer_phone': customers[4]
                }
                dataList.append(c_object)
            data = json.dumps(dataList, sort_keys=True, indent=4, separators=(',', ': '))
        except Exception as e:
            data = ("Get Customer failed with error: {0}").format(e)
            db.rollback()
            print(data)

        cursor.close()
        db.close()
        return data

#==============================================================================
#   function: get_customer_for_flight
#   description: returns all customers with an inputted flight_id
#   return: customer json object(s)
#==============================================================================
    def get_customer_for_flight(self, flight_id):
        db = MySQLdb.connect(host=self.host,
                             user=self.user,
                             passwd=self.pw,
                             db=self.db)
        get_customer_query = """SELECT I.C_ID, S.F_ID
                                FROM ITINERARY I, SCHEDULE S
                                WHERE S.F_ID = %d AND S.I_ID = I.I_ID""" % (int(flight_id))

        cursor = db.cursor()
        try:
            dataList = []
            cursor.execute(get_customer_query)
            customers = cursor.fetchall()
            for c in customers:
                customer = {
                    'customer_id': c[0],
                    'flight_id': c[1]
                }
                dataList.append(customer)
            data = json.dumps(dataList, sort_keys=True, indent=4, separators=(',', ': '))
        except Exception as err:
            data = ("Get Customers For Flight failed with error: {0}").format(err)
            db.rollback()
            print(data)

        cursor.close()
        db.close()
        return data

#==============================================================================
#   function: add_customer
#   description: adds an instance of customer to CUSTOMER table
#   return: added customer JSON object
#==============================================================================
    def add_customer(self, cust_name, cust_age, cust_email, cust_phone):
        db = MySQLdb.connect(host=self.host,
                            user=self.user,
                            passwd=self.pw,
                            db=self.db)

        add_customer_query = """INSERT INTO CUSTOMER(C_NAME, C_AGE, C_EMAIL, C_PHONE)
                                VALUES('%s',%d,'%s','%s')""" % (cust_name, int(cust_age),
                                cust_email, cust_phone)
        cursor = db.cursor()
        try:
            cursor.execute(add_customer_query)
            db.commit()
            customer = {
                'customer_id': cursor.lastrowid,
                'customer_name': cust_name,
                'customer_age': int(cust_age),
                'customer_email': cust_email,
                'customer_phone': cust_phone
            }
            data = json.dumps(customer, sort_keys=True, indent=4, separators=(',', ': '))
        except Exception as e:
            data = ("Add Customer Failed with error: {0}").format(e)
            db.rollback()
            print(data)

        cursor.close()
        db.close()
        return data

#==============================================================================
#   function: update_customer
#   description: update the customer information
#==============================================================================
    def update_customer(self, customer_id, cust_field, new_value):
        db = MySQLdb.connect(host=self.host,
                             user=self.user,
                             passwd=self.pw,
                             db=self.db)
        update_customer_query = """UPDATE CUSTOMER
                                   SET %s = %s
                                   WHERE C_ID = %s""" % (cust_field, new_value, customer_id)

        cursor = db.cursor()
        try:
            cursor.execute(update_customer_query)
            db.commit()
            print('Update Customer Success')
            db.close()
            return 200

        except:
            print('Update Customer Failed')
            db.close()

            return 500

#==============================================================================
#   function: add_frequent_flier
#   description: adds a new frequent flier instance to FREQUENTFLIER table
#   return: added frequent flier json object
#==============================================================================
    def add_frequent_flier(self, customer_id):
        db = MySQLdb.connect(host=self.host,
                             user=self.user,
                             passwd=self.pw,
                             db=self.db)

        add_ff_query = """ INSERT INTO FREQUENTFLIER (C_ID, FF_MILES)
                           VALUES (%d, 0.0)""" % int(customer_id)

        cursor = db.cursor()
        try:
            cursor.execute(add_ff_query)
            db.commit()
            newff = {
                'customer_id': customer_id,
                'frequentflier_miles': 0.0,
            }
            data = json.dumps(newff, sort_keys=True, indent=4, separators=(',', ': '))
        except Exception as e:
            data = ("Add Frequent Flier Failed with error: {0}").format(e)
            db.rollback()
            print(data)

        cursor.close()
        db.close()
        return data

#==============================================================================
#   function: get_frequent_flier
#   description: get miles for customer
#==============================================================================
    def get_frequent_flier(self, customer_id):
        db = MySQLdb.connect(host=self.host,
                             user=self.user,
                             passwd=self.pw,
                             db=self.db)
        get_ff_query = """ SELECT FF_MILES FROM FREQUENTFLIER WHERE C_ID = %d """ % (int(customer_id))
        cursor = db.cursor()
        try:
            dataList = []
            cursor.execute(get_ff_query)
            db.commit()
            ff = cursor.fetchone()
            ff_object = {'frequentflier_miles': ff[0]}
            dataList.append(ff_object)
            data = json.dumps(dataList, sort_keys=True, indent=4, separators=(',', ': '))
        except Exception as e:
            data = ("Get Frequent Flier Failed with error: {0}").format(e)
            db.rollback()
            print(data)

        cursor.close()
        db.close()
        return data


#==============================================================================
#   function: update_frequent_flier
#   description: updates miles on frequent flier account
#   return: returns updated ff object
#==============================================================================
    def update_frequent_flier(self, customer_id, miles):
        db = MySQLdb.connect(host=self.host,
                             user=self.user,
                             passwd=self.pw,
                             db=self.db)
        cursor = db.cursor()
        try:
            cursor.execute("""SELECT FF_MILES FROM FREQUENTFLIER WHERE C_ID = %d """ % (int(customer_id)))
            old_miles = cursor.fetchone()
        except Exception as e:
            data = ("Update Frequent Flier Failed with error: {0}").format(e)
            return data

        new_miles = old_miles[0] + float(miles)
        update_ff_query = """UPDATE FREQUENTFLIER
                           SET FF_MILES = %.2f
                           WHERE C_ID = %d """ % (float(new_miles), int(customer_id))
        updated_ff = {
            'customer_id': customer_id,
            'frequentflier_miles': new_miles
        }
        try:
            cursor.execute(update_ff_query)
            db.commit()
            data = json.dumps(updated_ff, sort_keys=True, indent=4, separators=(',', ': '))
        except Exception as e:
            data = ("Update Frequent Flier Failed with error: {0}").format(e)
            db.rollback()
            print(data)

        cursor.close()
        db.close()
        return data

#==============================================================================
#   function: add_itinerary
#   description: add a new row to ITINERARY table
#   return: added Itinerary object
#==============================================================================
    def add_itinerary(self, seat_type, seat_cost, itinerary_status, customer_id):
        db = MySQLdb.connect(host=self.host, user=self.user, passwd=self.pw, db=self.db)

        add_itinerary_query = """ INSERT INTO ITINERARY (I_SEATTYPE, I_SEATCOST, I_STATUS, C_ID)
                              VALUES ('%s',%.2f, '%s', %d)""" % (seat_type, float(seat_cost),
                                                                itinerary_status, int(customer_id))

        cursor = db.cursor()
        try:
            cursor.execute(add_itinerary_query)
            db.commit()
            new_itinerary = {
                'itinerary_id': cursor.lastrowid,
                'seattype': seat_type,
                'seatcost': seat_cost,
                'status': itinerary_status,
                'customer_id': customer_id
            }
            data = json.dumps(new_itinerary, sort_keys=True, indent=4, separators=(',', ': '))
        except Exception as e:
            data = ("Add Itinerary Failed with error: {0}").format(e)
            db.rollback()
            print(data)

        db.close()
        cursor.close()
        return data

#==============================================================================
#   function: get_old_itinerary
#   description: get itinerary by customer ID that are 'DONE'
#   return: list of itineraries
#==============================================================================
    def get_old_itinerary(self, customer_id):
        db = MySQLdb.connect(host=self.host, user=self.user, passwd=self.pw, db=self.db)

        get_itinerary_query = """SELECT * FROM ITINERARY WHERE C_ID = %s AND I_STATUS = 'DONE' """ % customer_id
        cursor = db.cursor()

        try:
            dataList = []
            cursor.execute(get_itinerary_query)
            itineraries = cursor.fetchall()
            for itinerary in itineraries:
                it_object = {
                    'itinerary_id': itinerary[0],
                    'seattype': itinerary[1],
                    'seatcost': itinerary[2],
                    'status': itinerary[3]
                }
                dataList.append(it_object)
            data = json.dumps(dataList, sort_keys=True, indent=4, separators=(',', ': '))
        except Exception as e:
            print("Get Itinerary failed with error: {0}").format(e)
            db.rollback()
            data = 0

        cursor.close()
        db.close()
        return data


#==============================================================================
#   function: get_itinerary
#   description: get itinerary by customer ID
#   return: list of itineraries
#==============================================================================
    def get_itinerary(self, customer_id):
        db = MySQLdb.connect(host=self.host, user=self.user, passwd=self.pw, db=self.db)

        get_itinerary_query = """SELECT * FROM ITINERARY WHERE C_ID = %s""" % customer_id
        cursor = db.cursor()

        try:
            dataList = []
            cursor.execute(get_itinerary_query)
            itineraries = cursor.fetchall()
            for itinerary in itineraries:
                it_object = {
                    'itinerary_id': itinerary[0],
                    'seattype': itinerary[1],
                    'seatcost': itinerary[2],
                    'status': itinerary[3]
                }
                dataList.append(it_object)
            data = json.dumps(dataList, sort_keys=True, indent=4, separators=(',', ': '))
        except Exception as e:
            print("Get Itinerary failed with error: {0}").format(e)
            db.rollback()
            data = 0

        cursor.close()
        db.close()
        return data

#==============================================================================
#   function: check_itinerary
#   description: check if itinerary_id exists for customer_id
#   return: yes or no
#==============================================================================
    def check_itinerary(self, customer_id, itinerary_id):
        db = MySQLdb.connect(host=self.host, user=self.user, passwd=self.pw, db=self.db)

        get_itinerary_query = """SELECT * FROM ITINERARY WHERE C_ID = %d""" % (int(customer_id))
        cursor = db.cursor()
        try:
            cursor.execute(get_itinerary_query)
            itineraries = cursor.fetchall()
            for itinerary in itineraries:
                if itinerary[0] == int(itinerary_id):
                    return 1
        except Exception as e:
            print("Check Itinerary failed with error: {0}").format(e)
            db.rollback()

        cursor.close()
        db.close()
        return 0

#==============================================================================
#   function: get_destination_for_itinerary
#   description: get destination city based on itinerary id
#   return: a destination city
#==============================================================================
    def get_destination_for_itinerary(self, itinerary_id):
        db = MySQLdb.connect(host=self.host, user=self.user, passwd=self.pw, db=self.db)
        get_destination_query = """select A2.AP_CITY from ITINERARY I, SCHEDULE S, FLIGHT F, AIRPORT A1, AIRPORT A2 where I.I_ID = S.I_ID
                                and S.F_ID = F.F_ID and A1.AP_ID = F.F_DEPARTUREAIRPORTID and A2.AP_ID = F.F_ARRIVALAIRPORTID
                                and I.I_ID = %d ORDER BY F.F_ARRIVALTIME DESC LIMIT 1;""" % (int(itinerary_id))
        cursor = db.cursor()

        try:
            dataList = []
            cursor.execute(get_destination_query)
            destination = cursor.fetchone()
            if destination is not None:
                data = {
                    'destination': destination[0]
                }
            else :
                data = {
                    'destination': 'None'
                }
            data = json.dumps(data, sort_keys=True, indent=4, separators=(',', ': '))
        except Exception as e:
            print("Get Itinerary destination failed with error: {0}").format(e)
            db.rollback()
            data = 0

        cursor.close()
        db.close()
        return data

#==============================================================================
#   function: get_itinerary_distance
#   description: get total distance of trip (by customer id)
#   return: itinerary table and float of total trip distance
#==============================================================================
    def get_itinerary_with_distance(self, customer_id):
        db = MySQLdb.connect(host=self.host,
                            user=self.user,
                            passwd=self.pw,
                            db=self.db)

        get_distance_query = """SELECT I.*, SUM(F_DISTANCE)
                                FROM FLIGHT F, SCHEDULE S, ITINERARY I
                                WHERE I.C_ID = %d and I.I_ID = S.I_ID and S.F_ID = F.F_ID
                                GROUP BY I.I_ID""" % (int(customer_id))
        cursor = db.cursor()
        try:
            dataList = []
            cursor.execute(get_distance_query)
            itineraries = cursor.fetchall()
            for itinerary in itineraries:
                distance_object = {
                    'itinerary_id': int(itinerary[0]),
                    'seattype': itinerary[1],
                    'seatcost': itinerary[2],
                    'status': itinerary[3],
                    'total_distance': float(itinerary[5]),
                }
                dataList.append(distance_object)
            data = json.dumps(dataList, sort_keys=True, indent=4, separators=(',', ': '))
        except Exception as err:
            data = ("Get Total Distance Failed with error: {0}").format(err)
            print(data)
            db.rollback()

        cursor.close()
        db.close()
        return data

#==============================================================================
#   function: get_customer_itinerary_info
#   description: query for Specific Itinerary tab in User UI
#   return: list of itineraries
#==============================================================================
    def get_customer_itinerary_info(self, itinerary_id):
        db = MySQLdb.connect(host=self.host, user=self.user, passwd=self.pw, db=self.db)

        get_itinerary_query = """select F.F_ID, A1.AP_CITY, F.F_DEPARTURETIME, A2.AP_CITY, F.F_ARRIVALTIME, F.F_STATUS
                                  from ITINERARY I, SCHEDULE S, FLIGHT F, AIRPORT A1, AIRPORT A2
                                  where I.I_ID = S.I_ID and S.F_ID = F.F_ID and A1.AP_ID = F.F_DEPARTUREAIRPORTID and A2.AP_ID = F.F_ARRIVALAIRPORTID
                                  and I.I_ID = %d ORDER BY F.F_ARRIVALTIME asc""" % (int(itinerary_id))
        cursor = db.cursor()
        try:
            dataList = []
            cursor.execute(get_itinerary_query)
            itineraries = cursor.fetchall()
            for itinerary in itineraries:
                it_object = {
                    'flight_id': itinerary[0],
                    'departure_city': itinerary[1],
                    'departure_time': itinerary[2],
                    'arrival_city': itinerary[3],
                    'arrival_time': itinerary[4],
                    'status': itinerary[5]
                }
                dataList.append(it_object)
            data = json.dumps(dataList, sort_keys=True, indent=4, separators=(',', ': '))
        except Exception as e:
            print("Get Itinerary failed with error: {0}").format(e)
            db.rollback()
            data = 0

        cursor.close()
        db.close()
        return data

#==============================================================================
#   function: get_schedule_for_employee
#   description: query for flight schedule table in Employee UI
#   return: list of flights
#==============================================================================
    def get_schedule_for_employee(self, employee_id):
        db = MySQLdb.connect(host=self.host, user=self.user, passwd=self.pw, db=self.db)

        get_emp_schedule_query = """ SELECT F.F_ID, A1.AP_CITY, F.F_DEPARTURETIME, A2.AP_CITY, F.F_ARRIVALTIME, F.F_STATUS
                                     FROM WORKSON W, FLIGHT F, AIRPORT A1, AIRPORT A2
                                     WHERE W.F_ID = F.F_ID and F.F_DEPARTUREAIRPORTID = A1.AP_ID and F.F_ARRIVALAIRPORTID = A2.AP_ID
                                     and W.E_ID = %d ORDER BY F.F_DEPARTURETIME """ % (int(employee_id))
        cursor = db.cursor()
        try:
            dataList = []
            cursor.execute(get_emp_schedule_query)
            flights = cursor.fetchall()
            for flight in flights:
                f_object = {
                    'flight_id': flight[0],
                    'departure_city': flight[1],
                    'departure_time': flight[2],
                    'arrival_city': flight[3],
                    'arrival_time': flight[4],
                    'status': flight[5]
                }
                dataList.append(f_object)
            data = json.dumps(dataList, sort_keys=True, indent=4, separators=(',', ': '))
        except Exception as e:
            print("Get Employee Schedule failed with error: {0}").format(e)
            db.rollback()
            data = 0

        cursor.close()
        db.close()
        return data

#==============================================================================
#   function: delete_itinerary
#   description: delete itinerary given itinerary ID
#   return: deleted itinerary id
#==============================================================================
    def delete_itinerary(self, itinerary_id):
        db = MySQLdb.connect(host=self.host, user=self.user, passwd=self.pw, db=self.db)

        delete_itinerary_query = """ DELETE FROM ITINERARY WHERE I_ID = %d """ % int(itinerary_id)

        cursor = db.cursor()
        deleted_itinerary_id = {
            'itinerary_id': int(itinerary_id)
        }
        try:
            get_itinerary_query = """SELECT I_STATUS FROM ITINERARY WHERE I_ID = %d""" % (int(itinerary_id))
            cursor.execute(get_itinerary_query)
            check_itinerary = cursor.fetchone()
            if check_itinerary[0] == 'DONE':
                data = 1
            else:
                cursor.execute(delete_itinerary_query)
                db.commit()
                data = json.dumps(deleted_itinerary_id, sort_keys=True, indent=4, separators=(',', ': '))
        except Exception as e:
            print("Delete Itinerary Failed with error: {0}".format(e))
            db.rollback()
            data = 0

        cursor.close()
        db.close()
        return data

#==============================================================================
#   function: update_itinerary
#   description: update itinerary fields given itinerary ID
#==============================================================================
    def update_itinerary(self, itinerary_id, itinerary_field, new_value):
        db = MySQLdb.connect(host=self.host,
                             user=self.user,
                             passwd=self.pw,
                             db=self.db)

        update_itinerary_query = """UPDATE ITINERARY
                                    SET %s = %s
                                    WHERE I_ID = %d """ % (itinerary_field, new_value, int(itinerary_id))

        cursor = db.cursor()
        try:
            get_itinerary_status = """SELECT I_STATUS FROM ITINERARY WHERE I_ID = %d""" % (int(itinerary_id))
            cursor.execute(get_itinerary_status)
            check_itinerary = cursor.fetchone()
            if check_itinerary[0] == 'DONE':
                data = 1
            else:
                cursor.execute(update_itinerary_query)
                db.commit()
                get_itinerary_query = """SELECT * FROM ITINERARY WHERE I_ID = %s""" % (itinerary_id)
                cursor.execute(get_itinerary_query)
                updated_itinerary = cursor.fetchone()
                updated_itinerary_object = {
                    'itinerary_id': updated_itinerary[0],
                    'seattype': updated_itinerary[1],
                    'seatcost': float(updated_itinerary[2]),
                    'status': updated_itinerary[3],
                    'customer_id': updated_itinerary[4]
                }
                data = json.dumps(updated_itinerary_object, sort_keys=True, indent=4, separators=(',', ': '))
        except Exception as e:
            print("Update Itinerary Failed with error: {0}".format(e))
            db.rollback()
            data = 0

        cursor.close()
        db.close()
        return data

#==============================================================================
#   function: add_flight
#   description: add new flight to FLIGHT table
#==============================================================================
    def add_flight(self, aircraft_id, distance, departtime, arrivetime, departairport, arriveairport,
                   departgate, arrivegate, status):
        db = MySQLdb.connect(host=self.host, user=self.user, passwd=self.pw, db=self.db)

        add_flight_query = """ INSERT INTO FLIGHT (AC_ID, F_DISTANCE, F_DEPARTURETIME, F_ARRIVALTIME,
                               F_DEPARTUREAIRPORTID, F_ARRIVALAIRPORTID, F_DEPARTUREGATEID, F_ARRIVALGATEID,
                               F_STATUS) VALUES (%d, %.2f, '%s', '%s', '%s','%s','%s','%s','%s')""" % (int(aircraft_id),
                                float(distance), departtime, arrivetime, departairport, arriveairport, departgate,
                                arrivegate, status)

        cursor = db.cursor()
        try:
            cursor.execute(add_flight_query)
            db.commit()
            new_flight = {
                'flight_id': cursor.lastrowid,
                'aircraft_id': int(aircraft_id),
                'distance': float(distance),
                'departtime': departtime,
                'arrivetime': arrivetime,
                'departairport': departairport,
                'arriveairport': arriveairport,
                'departgate': departgate,
                'arrivegate': arrivegate,
                'status': status
            }
            data = json.dumps(new_flight, sort_keys=True, indent=4, separators=(',', ': '))
        except Exception as e:
            data = ("Add Flight Failed with error: {0}").format(e)
            db.rollback()
            print(data)

        cursor.close()
        db.close()
        return data

#==============================================================================
#   function: update_flight
#   description: update fields in FLIGHT given flight ID
#==============================================================================
    def update_flight(self, flight_id, flight_field, new_value):
        db = MySQLdb.connect(host=self.host,
                             user=self.user,
                             passwd=self.pw,
                             db=self.db)

        update_flight_query = """UPDATE FLIGHT
                                SET %s = %s
                                WHERE F_ID = %d """ % (flight_field, new_value, int(flight_id))

        cursor = db.cursor()
        try:
            cursor.execute(update_flight_query)
            db.commit()
            get_flight_query = """SELECT * FROM FLIGHT WHERE F_ID = %d""" % (int(flight_id))
            cursor.execute(get_flight_query)
            updated_flight = cursor.fetchone()
            updated_flight_object = {
                'flight_id': int(updated_flight[0]),
                'aircraft_id': int(updated_flight[1]),
                'distance': float(updated_flight[2]),
                'departtime': updated_flight[3],
                'arrivetime': updated_flight[4],
                'departairport': updated_flight[5],
                'arriveairport': updated_flight[6],
                'departgate': updated_flight[7],
                'arrivegate': updated_flight[8],
                'status': updated_flight[9]
            }
            data = json.dumps(updated_flight_object, sort_keys=True, indent=4, separators=(',', ': '))
        except Exception as e:
            print("Update Flight Failed with error: {0}".format(e))
            db.rollback()
            data = 0

        cursor.close()
        db.close()
        return data

#==============================================================================
#   function: get_flight
#   description: get all flights or a given flight ID
#   returns: the list of all flights if there are no specified Flight_id
#        or: the flight corresponding to the given Flight_id
#==============================================================================
    def get_flight(self, f_id):
        db = MySQLdb.connect(host=self.host,
                            user=self.user,
                            passwd=self.pw,
                            db=self.db)

        get_flight_query = ""
        if f_id is None:
            get_flight_query = """SELECT * FROM FLIGHT"""
        else:
            get_flight_query = """SELECT * FROM FLIGHT WHERE F_ID = '%s'""" % (f_id)
        cursor = db.cursor()
        try:
            dataList = []
            cursor.execute(get_flight_query)
            if f_id is None:
                flights = cursor.fetchall()
                for flight in flights:
                    f_object = {
                        'flight_id': int(flight[0]),
                        'aircraft_id': int(flight[1]),
                        'distance': float(flight[2]),
                        'departtime': flight[3],
                        'arrivetime': flight[4],
                        'departairport': flight[5],
                        'arriveairport': flight[6],
                        'departgate': flight[7],
                        'arrivegate': flight[8],
                        'status': flight[9]
                    }
                    dataList.append(f_object)
            else:
                flights = cursor.fetchone()
                f_object = {
                        'flight_id': int(flights[0]),
                        'aircraft_id': int(flights[1]),
                        'distance': float(flights[2]),
                        'departtime': flights[3],
                        'arrivetime': flights[4],
                        'departairport': flights[5],
                        'arriveairport': flights[6],
                        'departgate': flights[7],
                        'arrivegate': flights[8],
                        'status': flights[9]
                }
                dataList.append(f_object)
            data = json.dumps(dataList, sort_keys = True, indent = 4, separators = (',', ': '))
        except Exception as e:
            print("Get Flight Failed with error: {0}").format(e)
            db.rollback()
            data = 0

        cursor.close()
        db.close()
        return data

#==============================================================================
#   function: get_flight
#   description: get all flights or a given flight ID
#   returns: the list of all flights if there are no specified Flight_id
#        or: the flight corresponding to the given Flight_id
#==============================================================================
    def get_flight_for_a_day(self, datestring):
        db = MySQLdb.connect(host=self.host,
                             user=self.user,
                             passwd=self.pw,
                             db=self.db)
        start_date = datetime.strptime(datestring, "%m-%d-%Y")
        end_date = start_date + timedelta(days=1)
        end_date_string = end_date.strftime("%m-%d-%Y")
        get_flight_query = ("""select * from FLIGHT where STR_TO_DATE(F_DEPARTURETIME, '%m-%d-%Y:%H:%i') >= STR_TO_DATE('{0}', '%m-%d-%Y')
                            and STR_TO_DATE(F_DEPARTURETIME, '%m-%d-%Y:%H:%i') <= STR_TO_DATE('{1}', '%m-%d-%Y')""").format(datestring, end_date_string)
        cursor = db.cursor()
        try:
            dataList = []
            cursor.execute(get_flight_query)
            flights = cursor.fetchall()
            for flight in flights:
                f_object = {
                    'flight_id': int(flight[0]),
                    'aircraft_id': int(flight[1]),
                    'distance': float(flight[2]),
                    'departtime': flight[3],
                    'arrivetime': flight[4],
                    'departairport': flight[5],
                    'arriveairport': flight[6],
                    'departgate': flight[7],
                    'arrivegate': flight[8],
                    'status': flight[9]
                }
                dataList.append(f_object)
            data = json.dumps(dataList, sort_keys = True, indent = 4, separators = (',', ': '))
        except Exception as e:
            print("Get Flight of date Failed with error: {0}").format(e)
            db.rollback()
            data = 0

        cursor.close()
        db.close()
        return data

#==============================================================================
#   function: get_delayed_flight
#   description: get all flights that are delayed
#   returns: the list of all flights where status = 'delayed'
#==============================================================================
    def get_delayed_flight(self):
        db = MySQLdb.connect(host=self.host,
                            user=self.user,
                            passwd=self.pw,
                            db=self.db)


        get_delayed_flight_query = """SELECT * FROM DELAYED_FLIGHT"""
        cursor = db.cursor()
        try:
            dataList = []
            cursor.execute(get_delayed_flight_query)
            flights = cursor.fetchall()
            for flight in flights:
                f_object = {
                    'flight_id': int(flight[0]),
                    'aircraft_id': int(flight[1]),
                    'distance': float(flight[2]),
                    'departtime': flight[3],
                    'arrivetime': flight[4],
                    'departairport': flight[5],
                    'arriveairport': flight[6],
                    'departgate': flight[7],
                    'arrivegate': flight[8],
                    'status': flight[9]
                }
                dataList.append(f_object)
            data = json.dumps(dataList, sort_keys = True, indent = 4, separators = (',', ': '))
        except Exception as e:
            print("Get Delayed Flight Failed with error: {0}").format(e)
            db.rollback()
            data = 0

        cursor.close()
        db.close()
        return data

#==============================================================================
#   function: get_flight_for_day
#   description: get all the flights for a certain departure/arrival day in
#               table FLIGHT
#   returns: the list of all the flights with departure/arrival time including
#           the inputted day
#==============================================================================
    def get_flight_for_day(self, day, dept_or_arrv):
        db = MySQLdb.connect(host=self.host,
                             user=self.user,
                             passwd=self.pw,
                             db=self.db)

        if dept_or_arrv == "dept":
            dept_or_arrv_field = 'F_DEPARTURETIME'
        elif dept_or_arrv == "arrv":
            dept_or_arrv_field = 'F_ARRIVALTIME'
        else:
            return "Departure or Arrival input is not recognized"

        dept_or_arrv_day = '{0}%'.format(day)
        get_flight_query = """SELECT *
                                FROM FLIGHT WHERE %s LIKE
                                '%s'""" % (dept_or_arrv_field, dept_or_arrv_day)

        cursor = db.cursor()
        try:
            dataList = []
            cursor.execute(get_flight_query)
            flights = cursor.fetchall()
            for flight in flights:
                f_object = {
                    'flight_id': int(flight[0]),
                    'aircraft_id': int(flight[1]),
                    'distance': float(flight[2]),
                    'departtime': flight[3],
                    'arrivetime': flight[4],
                    'departairport': flight[5],
                    'arriveairport': flight[6],
                    'departgate': flight[7],
                    'arrivegate': flight[8],
                    'status': flight[9]
                }
                dataList.append(f_object)
            data = json.dumps(dataList, sort_keys=True, indent=4, separators=(',', ': '))
        except Exception as err:
            data = 'Get Flights For Day Failed with error: {0}'.format(err)
            db.rollback()
            print(data)

        cursor.close()
        db.close()
        return data

#==============================================================================
#   function: get_flight_for_airport
#   description: get all departing/arriving flights for an aircraft in an airport
#   returns: the list of all departing/arriving flights based on the inputted
#        departing/arriving parameter, aircraft id, and airport id
#==============================================================================
    def get_flight_for_airport(self, ap_id, dept_or_arrv):
        db = MySQLdb.connect(host=self.host,
                            user=self.user,
                            passwd=self.pw,
                            db=self.db)

        if dept_or_arrv == "dept":
            dept_or_arrv_airport = 'F_DEPARTUREAIRPORTID'
        elif dept_or_arrv == "arrv":
            dept_or_arrv_airport = 'F_ARRIVALAIRPORTID'
        else:
            return "Departure or Arrival input is not recognized"

        get_flight_query = """SELECT F_ID, AC_ID, F_DISTANCE, F_DEPARTURETIME, F_DEPARTUREAIRPORTID,
                            F_DEPARTUREGATEID, F_ARRIVALTIME, F_ARRIVALAIRPORTID, F_ARRIVALGATEID,
                            F_STATUS FROM FLIGHT WHERE %s = '%s'""" % (dept_or_arrv_airport, ap_id)

        cursor = db.cursor()
        try:
            dataList = []
            cursor.execute(get_flight_query)
            flights = cursor.fetchall()
            for flight in flights:
                f_object = {
                    'flight_id': int(flight[0]),
                    'aircraft_id': int(flight[1]),
                    'distance': float(flight[2]),
                    'departtime': flight[3],
                    'departairport': flight[4],
                    'departgate': flight[5],
                    'arrivetime': flight[6],
                    'arriveairport': flight[7],
                    'arrivegate': flight[8],
                    'status': flight[9]
                }
                dataList.append(f_object)
            data = json.dumps(dataList, sort_keys=True, indent=4, separators=(',', ': '))
        except Exception as err:
            print('Get Flights For Airport Failed with error: {0}'.format(err))
            db.rollback()
            data = 0

        cursor.close()
        db.close()
        return data

#==============================================================================
#   function: get_airport
#   description: get all the airports
#   returns: the list of all the airports if there are no specified Airport_id
#        or: the airport where aiport_id matches the inputted airport_id
#==============================================================================
    def get_airport(self, ap_id):
        db = MySQLdb.connect(host=self.host,
                            user=self.user,
                            passwd=self.pw,
                            db=self.db)

        get_airport_query = ""
        if ap_id is None:
            get_airport_query = """SELECT * FROM AIRPORT"""
        else:
            get_airport_query = """SELECT * FROM AIRPORT WHERE AP_ID = '%s'""" % (ap_id)
        cursor = db.cursor()
        try:
            dataList = []
            cursor.execute(get_airport_query)
            if ap_id is None:
                airports = cursor.fetchall()
                for airport in airports:
                    ap_object = {
                        'airport_id': airport[0],
                        'city': airport[1],
                        'country': airport[2]
                    }
                    dataList.append(ap_object)
            else:
                airports = cursor.fetchone()
                ap_object = {
                    'airport_id': airports[0],
                    'city': airports[1],
                    'country': airports[2]
                }
                dataList.append(ap_object)
            data = json.dumps(dataList, sort_keys=True, indent=4, separators=(',', ': '))
        except Exception as e:
            print("Get Airport Failed with error: {0}").format(e)
            db.rollback()
            data = 0

        cursor.close()
        db.close()
        return data

#==============================================================================
#   function: add_airport
#   description: add an airport instance to the AIRPORT table
#==============================================================================
    def add_airport(self, ap_id, ap_city, ap_country):
        db = MySQLdb.connect(host=self.host,
                            user=self.user,
                            passwd=self.pw,
                            db=self.db)

        add_airport_query = """INSERT INTO AIRPORT(AP_ID, AP_CITY, AP_COUNTRY)
                                VALUES('%s', '%s', '%s')""" % (ap_id,
                                ap_city, ap_country)
        cursor = db.cursor()
        airport = {
            'airport_id': ap_id,
            'city': ap_city,
            'country': ap_country
        }
        try:
            cursor.execute(add_airport_query)
            db.commit()
            data = json.dumps(airport, sort_keys=True, indent=4, separators=(',', ': '))
        except Exception as e:
            data = ("Add Airport Failed with error: {0}").format(e)
            db.rollback()

        cursor.close()
        db.close()
        return data

#==============================================================================
#   function: delete_airport
#   description: delete an airport from the airport table
#==============================================================================
    def delete_airport(self, ap_id):
        db = MySQLdb.connect(host=self.host,
                            user=self.user,
                            passwd=self.pw,
                            db=self.db)

        delete_airport_query = """DELETE FROM AIRPORT WHERE AP_ID = '%s'""" % (ap_id)
        cursor = db.cursor()
        deleted_airport_id = {
            'airport_id': ap_id
        }
        try:
            cursor.execute(delete_airport_query)
            db.commit()
            data = json.dumps(deleted_airport_id, sort_keys=True, indent=4, separators=(',', ': '))
        except Exception as e:
            data = ("Delete Airport Failed with error: {0}").format(e)
            print(data)
            db.rollback()

        cursor.close()
        db.close()
        return data

 #==============================================================================
 #   function: update_airport
 #   description: update an airport instance to the AIRPORT table
 #==============================================================================
    def update_airport(self, ap_id, field, new_value):
        db = MySQLdb.connect(host=self.host,
                             user=self.user,
                             passwd=self.pw,
                             db=self.db)
        update_airport_query = """UPDATE AIRPORT
                                SET %s = %s
                                WHERE AP_ID = '%s'""" % (field, new_value, ap_id)
        cursor = db.cursor()
        try:
            cursor.execute(update_airport_query)
            db.commit()
            data = ("Update Airport succeeded")
        except Exception as e:
            data = ("Update Airport Failed with error: {0}").format(e)
            print(data)
            db.rollback()

        cursor.close()
        db.close()
        return data

#==============================================================================
#   function: get_gates_of_airport
#   description: get all the gates from an airport
#   returns: the list of all the gates from a specified airport_id
#==============================================================================
    def get_gates_of_airport(self, ap_id):
         db = MySQLdb.connect(host=self.host,
                             user=self.user,
                             passwd=self.pw,
                             db=self.db)

         if ap_id is None:
             return "Airport ID is NULL"
         else:
             get_gate_query = """SELECT * FROM GATE WHERE AP_ID = '%s'""" % (ap_id)
         cursor = db.cursor()
         try:
             dataList = []
             cursor.execute(get_gate_query)
             gates = cursor.fetchall()
             for g in gates:
                 gate = {
                    'gate_id': g[0],
                    'airport_id': g[1]
                 }
                 dataList.append(gate)
             data = json.dumps(dataList, sort_keys=True, indent=4, separators=(',', ': '))
         except Exception as e:
             data = ("Get Airport Failed with error: {0}").format(e)
             db.rollback()
             print(data)

         cursor.close()
         db.close()
         return data

#==============================================================================
#   function: delete_gate
#   description: delete a gate with specified gate id and airport id
#==============================================================================
    def delete_gate(self, ap_id, g_id):
         db = MySQLdb.connect(host=self.host,
                             user=self.user,
                             passwd=self.pw,
                             db=self.db)

         delete_gate_query = """DELETE FROM GATE WHERE AP_ID = '%s' and G_ID = '%s'""" % (ap_id, g_id)
         cursor = db.cursor()
         deleted_gate = {
            'airport_id': ap_id,
            'gate_id': g_id
         }
         try:
             cursor.execute(delete_gate_query)
             db.commit()
             data = json.dumps(deleted_gate, sort_keys=True, indent=4, separators=(',', ': '))
         except Exception as e:
             data = ("Delete Gate Failed with error: {0}").format(e)
             print(data)
             db.rollback()

         cursor.close()
         db.close()
         return data


#==============================================================================
#   function: add_aircraft
#   description: add an aircraft instance to table AIRCRAFT
#   returns: the added aircraft json object
#==============================================================================
    def add_aircraft(self, status, make, mileage, datecreated, lastmaintained, economy,
                    business, firstclass, airport):
        db = MySQLdb.connect(host=self.host,
                            user=self.user,
                            passwd=self.pw,
                            db=self.db)

        add_aircraft_query = """INSERT INTO AIRCRAFT(AC_STATUS, AC_MAKE, AC_MILEAGE,
                                AC_DATE_CREATED, AC_LAST_MAINTAINED, AC_NUM_ECONOMY,
                                AC_NUM_BUSINESS, AC_NUM_FIRSTCLASS, AP_ID)
                                VALUES ('%s', '%s', %.2f, '%s', '%s', %d, %d, %d, '%s')""" % (
                                status, make, float(mileage), datecreated, lastmaintained,
                                int(economy), int(business), int(firstclass), airport)

        cursor = db.cursor()
        try:
            cursor.execute(add_aircraft_query)
            aircraft = {
                'id': cursor.lastrowid,
                'status': status,
                'make': make,
                'mileage': float(mileage),
                'date_created': datecreated,
                'last_maintained': lastmaintained,
                'num_economy': economy,
                'num_business': business,
                'num_firstclass': firstclass,
                'airport_id': airport
            }
            db.commit()
            data = json.dumps(aircraft, sort_keys=True, indent=4, separators=(',', ': '))
        except Exception as err:
            data = 'Add Aircraft Failed with error: {0}'.format(err)
            db.rollback()
            print(data)

        cursor.close()
        db.close()
        return data

#==============================================================================
#   function: get_aircraft
#   description: get all the aircrafts with specificed aircraft_id in
#       table AIRCRAFT
#   returns: the list of all aircrafts if there are no specified aircraft_id
#        or: the aircraft where aircraft_id matches the inputted aircraft_id
#==============================================================================
    def get_aircraft(self, ac_id):
        db = MySQLdb.connect(host=self.host,
                             user=self.user,
                             passwd=self.pw,
                             db=self.db)
        if ac_id is None:
            get_aircraft_query = """SELECT * FROM AIRCRAFT"""
        else:
            get_aircraft_query = """SELECT * FROM AIRCRAFT WHERE AC_ID = %d""" % (int(ac_id))
        cursor = db.cursor()
        try:
            dataList = []
            cursor.execute(get_aircraft_query)
            if ac_id is None:
                aircrafts = cursor.fetchall()
                for aircraft in aircrafts:
                    ac_object = {
                        'id': aircraft[0],
                        'status': aircraft[1],
                        'make': aircraft[2],
                        'mileage': float(aircraft[3]),
                        'date_created': aircraft[4],
                        'last_maintained': aircraft[5],
                        'num_economy': aircraft[6],
                        'num_business': aircraft[7],
                        'number_firstclass': aircraft[8],
                        'airport_id': aircraft[9]
                    }
                    dataList.append(ac_object)
            else:
                aircrafts = cursor.fetchone()
                ac_object = {
                    'id': aircrafts[0],
                    'status': aircrafts[1],
                    'make': aircrafts[2],
                    'mileage': float(aircrafts[3]),
                    'date_created': aircrafts[4],
                    'last_maintained': aircrafts[5],
                    'num_economy': aircrafts[6],
                    'num_business': aircrafts[7],
                    'number_firstclass': aircrafts[8],
                    'airport_id': aircrafts[9]
                }
                dataList.append(ac_object)
            data = json.dumps(dataList, sort_keys=True, indent=4, separators=(',', ': '))
        except Exception as err:
            data = 'Get Aircraft Failed with error: {0}'.format(err)
            db.rollback()
            print(data)

        cursor.close()
        db.close()
        return data

    def get_aircraft_by_airport(self, airport_id):
        db = MySQLdb.connect(host=self.host,
                             user=self.user,
                             passwd=self.pw,
                             db=self.db)
        get_aircraft_query = """SELECT * FROM AIRCRAFT WHERE AP_ID = '%s' """ % (airport_id)
        cursor = db.cursor()
        try:
            dataList = []
            cursor.execute(get_aircraft_query)
            aircrafts = cursor.fetchall()
            for aircraft in aircrafts:
                ac_object = {
                    'id': aircraft[0],
                    'status': aircraft[1],
                    'make': aircraft[2],
                    'mileage': float(aircraft[3]),
                    'date_created': aircraft[4],
                    'last_maintained': aircraft[5],
                    'num_economy': aircraft[6],
                    'num_business': aircraft[7],
                    'number_firstclass': aircraft[8],
                    'airport_id': aircraft[9]
                }
                dataList.append(ac_object)
            data = json.dumps(dataList, sort_keys=True, indent=4, separators=(',', ': '))
        except Exception as err:
            print('Get Aircraft by Airport ID Failed with error: {0}'.format(err))
            db.rollback()
            data = 0

        cursor.close()
        db.close()
        return data

    def get_aircraft_by_airport_total(self):
        db = MySQLdb.connect(host=self.host,
                             user=self.user,
                             passwd=self.pw,
                             db=self.db)
        get_aircraft_total_query = """ SELECT AIRPORT.*, COUNT(AIRCRAFT.AC_ID)
                                       FROM AIRPORT, AIRCRAFT
                                       WHERE AIRCRAFT.AP_ID = AIRPORT.AP_ID GROUP BY AIRPORT.AP_ID """
        cursor = db.cursor()
        try:
            dataList = []
            cursor.execute(get_aircraft_total_query)
            total = cursor.fetchall()
            for t in total:
                total_object = {
                    'airport_id': t[0],
                    'city': t[1],
                    'country': t[2],
                    'total_aircraft': int(t[3])
                }
                dataList.append(total_object)
            data = json.dumps(dataList, sort_keys=True, indent=4, separators=(',', ': '))
        except Exception as err:
            data = 'Get Total Aircraft by Airport Failed with error: {0}'.format(err)
            db.rollback()
            print(data)

        cursor.close()
        db.close()
        return data

    def get_aircraft_by_status(self, status):
        db = MySQLdb.connect(host=self.host,
                             user=self.user,
                             passwd=self.pw,
                             db=self.db)
        get_aircraft_query = """SELECT * FROM AIRCRAFT WHERE AC_STATUS = '%s' """ % (status)
        cursor = db.cursor()
        try:
            dataList = []
            cursor.execute(get_aircraft_query)
            aircrafts = cursor.fetchall()
            for aircraft in aircrafts:
                ac_object = {
                    'id': aircraft[0],
                    'status': aircraft[1],
                    'make': aircraft[2],
                    'mileage': float(aircraft[3]),
                    'date_created': aircraft[4],
                    'last_maintained': aircraft[5],
                    'num_economy': aircraft[6],
                    'num_business': aircraft[7],
                    'number_firstclass': aircraft[8],
                    'airport_id': aircraft[9]
                }
                dataList.append(ac_object)
            data = json.dumps(dataList, sort_keys=True, indent=4, separators=(',', ': '))
        except Exception as err:
            print('Get Aircraft by Status Failed with error: {0}'.format(err))
            db.rollback()
            data = 0

        cursor.close()
        db.close()
        return data

#==============================================================================
#   function: get_aircraft_last_maintained
#   description: get all the aircrafts sorted by date last maintained
#   returns: the list of all aircrafts sorted by AC_LAST_MAINTAINED
#==============================================================================

    def get_aircraft_last_maintained(self):
        db = MySQLdb.connect(host=self.host,
                             user=self.user,
                             passwd=self.pw,
                             db=self.db)
        get_aircraft_query = """SELECT * FROM AIRCRAFT
                                ORDER BY STR_TO_DATE(AC_LAST_MAINTAINED, '%m-%d-%Y') ASC"""
        cursor = db.cursor()
        try:
            dataList = []
            cursor.execute(get_aircraft_query)
            aircrafts = cursor.fetchall()
            for aircraft in aircrafts:
                ac_object = {
                    'id': aircraft[0],
                    'status': aircraft[1],
                    'make': aircraft[2],
                    'mileage': float(aircraft[3]),
                    'date_created': aircraft[4],
                    'last_maintained': aircraft[5],
                    'num_economy': aircraft[6],
                    'num_business': aircraft[7],
                    'number_firstclass': aircraft[8],
                    'airport_id': aircraft[9]
                }
                dataList.append(ac_object)
            data = json.dumps(dataList, sort_keys=True, indent=4, separators=(',', ': '))
        except Exception as err:
            data = 'Get Aircraft sorted by Last Maintained Failed with error: {0}'.format(err)
            db.rollback()
            print(data)

        cursor.close()
        db.close()
        return data

#==============================================================================
#   function: update_aircraft
#   description: update an aircraft's status in table AIRCRAFT
#   returns: the updated aircraft object in table AIRCRAFT
#==============================================================================
    def update_aircraft(self, ac_id, status):
        db = MySQLdb.connect(host=self.host,
                             user=self.user,
                             passwd=self.pw,
                             db=self.db)

        update_aircraft_query = """UPDATE AIRCRAFT SET AC_STATUS = %s
                                        WHERE AC_ID = %d""" % (status, int(ac_id))
        cursor = db.cursor()
        try:
            cursor.execute(update_aircraft_query)
            db.commit()
            get_aircraft_query = """SELECT * FROM AIRCRAFT WHERE AC_ID = %d""" % (int(ac_id))
            cursor.execute(get_aircraft_query)
            aircraft = cursor.fetchone()
            ac_object = {
                'id': aircraft[0],
                'status': aircraft[1],
                'make': aircraft[2],
                'mileage': float(aircraft[3]),
                'date_created': aircraft[4],
                'last_maintained': aircraft[5],
                'num_economy': aircraft[6],
                'num_business': aircraft[7],
                'num_firstclass': aircraft[8],
                'airport_id': aircraft[9]
            }
            data = json.dumps(ac_object, sort_keys=True, indent=4, separators=(',', ': '))
        except Exception as err:
            print('Update Aircraft Failed with error: {0}'.format(err))
            db.rollback()
            data = 0

        cursor.close()
        db.close()
        return data


#==============================================================================
#   function: delete_aircraft
#   description: delete an aircraft from table AIRCRAFT
#   returns: the deleted aircraft id
#==============================================================================
    def delete_aircraft(self, ac_id):
        db = MySQLdb.connect(host=self.host,
                            user=self.user,
                            passwd=self.pw,
                            db=self.db)

        delete_aircraft_query = """DELETE FROM AIRCRAFT WHERE AC_ID = %d""" % (int(ac_id))
        cursor = db.cursor()
        deleted_aircraft_id = {
            'ID': ac_id
        }
        try:
            cursor.execute(delete_aircraft_query)
            db.commit()
            data = json.dumps(deleted_aircraft_id, sort_keys=True, indent=4, separators=(',', ': '))
        except Exception as err:
            print('Delete Aircraft Failed with error: {0}'.format(err))
            db.rollback()
            data = 0

        cursor.close()
        db.close()
        return data

#==============================================================================
#   function: add_employee
#   description: add an employee instance to table EMPLOYEE
#   returns: the added employee json object
#==============================================================================
    def add_employee(self, hours, emp_type, emp_name, wage):
        db = MySQLdb.connect(host=self.host,
                            user=self.user,
                            passwd=self.pw,
                            db=self.db)

        add_employee_query = """INSERT INTO EMPLOYEE (E_HOURS, E_TYPE, E_NAME, E_WAGE)
                                VALUES (%.2f, '%s', '%s', %.2f)""" % (float(hours),
                                emp_type, emp_name, float(wage))

        cursor = db.cursor()
        try:
            cursor.execute(add_employee_query)
            employee = {
                'id': cursor.lastrowid,
                'hours': float(hours),
                'type': emp_type,
                'name': emp_name,
                'wage': float(wage)
            }
            db.commit()
            data = json.dumps(employee, sort_keys=True, indent=4, separators=(',', ': '))
        except Exception as err:
            print('Add Employee Failed with error: {0}'.format(err))
            db.rollback()
            data = 0

        cursor.close()
        db.close()
        return data

#==============================================================================
#   function: get_employee
#   description: get_employee by e_id or if e_id is None, return all employees
#   returns: employee with specified e_id or all employees
#==============================================================================
    def get_employee(self, e_id):
        db = MySQLdb.connect(host=self.host,
                            user=self.user,
                            passwd=self.pw,
                            db=self.db)
        if e_id is None:
            get_employee_query = """ SELECT * FROM EMPLOYEE """
        else:
            get_employee_query = """ SELECT * FROM EMPLOYEE WHERE E_ID = '%s' """ % (e_id)

        cursor = db.cursor()
        try:
            dataList = []
            cursor.execute(get_employee_query)
            if e_id is None:
                emps = cursor.fetchall()
                for emp in emps:
                    emp_object = {
                        'id': emp[0],
                        'hours': emp[1],
                        'type': emp[2],
                        'name': emp[3],
                        'wage': emp[4]
                    }
                    dataList.append(emp_object)
            else:
                emps= cursor.fetchone()
                emp_object = {
                    'id': emps[0],
                    'hours': emps[1],
                    'type': emps[2],
                    'name': emps[3],
                    'wage': emps[4]
                }
                dataList.append(emp_object)
            data = json.dumps(dataList, sort_keys=True, indent=4, separators=(',', ': '))
        except Exception as e:
            print("Get Employee Failed with error: {0}").format(e)
            db.rollback()
            data = 0

        cursor.close()
        db.close()
        return data

#==============================================================================
#   function: delete_employee
#   description: delete an employee from table EMPLOYEE
#   returns: the deleted employee id
#==============================================================================
    def delete_employee(self, e_id):
        db = MySQLdb.connect(host=self.host,
                            user=self.user,
                            passwd=self.pw,
                            db=self.db)

        delete_employee_query = """DELETE FROM EMPLOYEE WHERE E_ID = %d""" % (int (e_id))
        cursor = db.cursor()
        deleted_employee_id = {
            'id': e_id
        }
        try:
            cursor.execute(delete_employee_query)
            db.commit()
            data = json.dumps(deleted_employee_id, sort_keys=True, indent=4, separators=(',', ': '))
        except Exception as err:
            print('Delete Employee Failed with error: {0}'.format(err))
            db.rollback()
            data = 0

        cursor.close()
        db.close()
        return data

#==============================================================================
#   function: get_schedule_for_itinerary
#   description: get all the schedules with itinerary ID
#   returns: the list of all the schedules with a specified itinerary ID
#==============================================================================
    def get_schedule_for_itinerary(self, i_id):
        db = MySQLdb.connect(host=self.host,
                             user=self.user,
                             passwd=self.pw,
                             db=self.db)

        if i_id is None:
            get_schedule_query = """SELECT F_ID, ITINERARY.I_ID, C_ID, I_SEATTYPE, I_STATUS FROM SCHEDULE, ITINERARY
                                    WHERE ITINERARY.I_ID = SCHEDULE.I_ID"""
        else:
            get_schedule_query = """SELECT F_ID, ITINERARY.I_ID, C_ID, I_SEATTYPE, I_STATUS FROM SCHEDULE, ITINERARY
                                    WHERE ITINERARY.I_ID = SCHEDULE.I_ID AND ITINERARY.I_ID = %d""" % (int(i_id))
        cursor = db.cursor()
        try:
            dataList = []
            cursor.execute(get_schedule_query)
            schedules = cursor.fetchall()
            for schedule in schedules:
                s_object = {
                    'flight_id': schedule[0],
                    'itinerary_id': schedule[1],
                    'customer_id': schedule[2],
                    'seattype': schedule[3],
                    'status': schedule[4]
                }
                dataList.append(s_object)
            data = json.dumps(dataList, sort_keys=True, indent=4, separators=(',', ': '))
        except Exception as e:
            print("Get Schedules Failed with error: {0}".format(e))
            db.rollback()
            data = 0

        cursor.close()
        db.close()
        return data


#==============================================================================
#   function: get_schedule_for_customer
#   description: get all the schedules with custoer ID
#   returns: the list of all the schedules with a specified customer ID
#==============================================================================
    def get_schedule_for_customer(self, c_id):
        db = MySQLdb.connect(host=self.host,
                             user=self.user,
                             passwd=self.pw,
                             db=self.db)

        get_schedule_query = """SELECT F_ID, ITINERARY.I_ID, C_ID, I_SEATTYPE, I_STATUS FROM SCHEDULE, ITINERARY WHERE ITINERARY.I_ID = SCHEDULE.I_ID AND C_ID = %d""" % (int(c_id))
        cursor = db.cursor()
        try:
            dataList = []
            cursor.execute(get_schedule_query)
            if c_id is None:
                entireschedule = cursor.fetchall()
                for schedule in entireschedule:
                    s_object = {
                        'flight_id': schedule[0],
                        'itinerary_id': schedule[1],
                        'customer_id': schedule[2],
                        'seattype': schedule[3],
                        'status': schedule[4]
                    }
                    dataList.append(s_object)
            else:
                entireschedule = cursor.fetchall()
                for schedule in entireschedule:
                    s_object = {
                    'flight_id': schedule[0],
                    'itinerary_id': schedule[1],
                    'customer_id': schedule[2],
                    'seattype': schedule[3],
                    'status': schedule[4]
                    }
                    dataList.append(s_object)
            data = json.dumps(dataList, sort_keys=True, indent=4, separators=(',', ': '))
        except Exception as e:
            print("Get Schedules Failed with error: {0}".format(e))
            db.rollback()
            data = 0

        cursor.close()
        db.close()
        return data

#==============================================================================
#   function: add_workson
#   description: add an employee/flight pair instance to table workson
#   returns: the added workson json object
#==============================================================================
    def add_workson(self, e_id, f_id):
        db = MySQLdb.connect(host=self.host,
                            user=self.user,
                            passwd=self.pw,
                            db=self.db)

        add_workson_query = """INSERT INTO WORKSON VALUES (%d, %d)""" % (int(e_id),
                                int(f_id))

        cursor = db.cursor()
        workson = {
            'employee_id': e_id,
            'flight_id': f_id
        }
        try:
            cursor.execute(add_workson_query)
            db.commit()
            data = json.dumps(workson, sort_keys=True, indent=4, separators=(',', ': '))
        except Exception as err:
            print('Add Workson Failed with error: {0}'.format(err))
            db.rollback()
            data = 0

        cursor.close()
        db.close()
        return data

#==============================================================================
#   function: get_employee_for_flight
#   description: get all the employees on a certain flight ID in table WORKSON
#   returns: the list of all the employees with a specified flight ID
#==============================================================================
    def get_employee_for_flight(self, f_id):
        db = MySQLdb.connect(host=self.host,
                             user=self.user,
                             passwd=self.pw,
                             db=self.db)
        if f_id is None:
            return "Flight ID is NULL"
        else:
            get_employee_query = """SELECT E.E_ID, W.F_ID
                                    FROM EMPLOYEE E, WORKSON W WHERE
                                    E.E_ID = W.E_ID AND W.F_ID = %d""" % (int(f_id))
        cursor = db.cursor()
        try:
            dataList = []
            cursor.execute(get_employee_query)
            employees = cursor.fetchall()
            for e in employees:
                employee = {
                    'employee_id': e[0],
                    'flight_id' : e[1]
                }
                dataList.append(employee)
            data = json.dumps(dataList, sort_keys=True, indent=4, separators=(',', ': '))
        except Exception as err:
            data = 'Get Employees Failed with error: {0}'.format(err)
            db.rollback()
            print(data)

        cursor.close()
        db.close()
        return data

#==============================================================================
#   function: get_flight_for_employee
#   description: get all the flights for a certain employee ID in table WORKSON
#   returns: the list of all the flights for a specified employee with employee ID
#==============================================================================
    def get_flight_for_employee(self, e_id):
        db = MySQLdb.connect(host=self.host,
                             user=self.user,
                             passwd=self.pw,
                             db=self.db)
        if e_id is None:
            return "Employee ID is NULL"
        else:
            get_flight_query = """SELECT W.E_ID, F.F_ID
                                    FROM FLIGHT F, WORKSON W WHERE
                                    F.F_ID = W.F_ID AND W.E_ID = %d""" % (int(e_id))
        cursor = db.cursor()
        try:
            dataList = []
            cursor.execute(get_flight_query)
            flights = cursor.fetchall()
            for f in flights:
                flight = {
                    'employee_id': f[0],
                    'flight_id': f[1]
                }
                dataList.append(flight)
            data = json.dumps(dataList, sort_keys=True, indent=4, separators=(',', ': '))
        except Exception as err:
            data = 'Get Flights Failed with error: {0}'.format(err)
            db.rollback()
            print(data)

        cursor.close()
        db.close()
        return data

#==============================================================================
#   function: get_workson
#   description: gets the entire WORKSON table
#   returns: the table WORKSON
#==============================================================================
    def get_workson(self):
         db = MySQLdb.connect(host=self.host,
                             user=self.user,
                             passwd=self.pw,
                             db=self.db)

         get_workson_query = """SELECT * FROM WORKSON"""
         cursor = db.cursor()
         try:
             dataList = []
             cursor.execute(get_workson_query)
             worksons = cursor.fetchall()
             for w in worksons:
                 workson = {
                    'employee_id': w[0],
                    'flight_id': w[1]
                 }
                 dataList.append(workson)
             data = json.dumps(dataList, sort_keys=True, indent=4, separators=(',', ': '))
         except Exception as err:
             print("Get WorksOns Failed with error: {0}".format(err))
             db.rollback()
             data = 0

         cursor.close()
         db.close()
         return data

#==============================================================================
#   function: delete_workson
#   description: delete a workson relation instance from table WORKSON
#   returns: the deleted workson json object
#==============================================================================
    def delete_workson(self, e_id, f_id):
        db = MySQLdb.connect(host=self.host,
                            user=self.user,
                            passwd=self.pw,
                            db=self.db)

        delete_workson_query = """DELETE FROM WORKSON WHERE E_ID = %d and
                                F_ID = %d""" % (int (e_id), int (f_id))
        cursor = db.cursor()
        deleted_workson = {
            'employee_id': e_id,
            'flight_id': f_id
        }
        try:
            cursor.execute(delete_workson_query)
            db.commit()
            data = json.dumps(deleted_workson, sort_keys=True, indent=4, separators=(',', ': '))
        except Exception as err:
            data = 'Delete Workson Failed with error: {0}'.format(err)
            db.rollback()
            print(data)
            data = 0

        cursor.close()
        db.close()
        return data

#==============================================================================
#   function: add_schedule
#   description: create a schedule with a flight ID and itinerary ID
#   return: json object of added schedule
#==============================================================================
    def add_schedule(self, i_id, f_id):
         db = MySQLdb.connect(host=self.host,
                             user=self.user,
                             passwd=self.pw,
                             db=self.db)

         add_schedule_query = """INSERT INTO SCHEDULE VALUES (%d, %d)""" % (int(i_id), int(f_id))
         cursor = db.cursor()
         added_schedule = {
            'itinerary_id': i_id,
            'flight_id': f_id
         }
         try:
             cursor.execute(add_schedule_query)
             db.commit()
             data = json.dumps(added_schedule, sort_keys=True, indent=4, separators=(',', ': '))
         except Exception as e:
             print("Add Schedule Failed with error: {0}".format(e))
             print(data)
             db.rollback()
             data = 0

         cursor.close()
         db.close()
         return data

#==============================================================================
#   function: delete_schedule
#   description: delete a schedule with specified itinerary id and flight id
#   return: deleted schedule object
#==============================================================================
    def delete_schedule(self, i_id, f_id):
         db = MySQLdb.connect(host=self.host,
                             user=self.user,
                             passwd=self.pw,
                             db=self.db)

         delete_schedule_query = """DELETE FROM SCHEDULE WHERE I_ID = %d and F_ID = %d""" % (int(i_id), int(f_id))
         cursor = db.cursor()
         deleted_schedule = {
            'itinerary_id': i_id,
            'flight_id': f_id
         }
         try:
             cursor.execute(delete_schedule_query)
             db.commit()
             data = json.dumps(deleted_schedule, sort_keys=True, indent=4, separators=(',', ': '))
         except Exception as e:
             print("Delete Schedule Failed with error: {0}".format(e))
             db.rollback()
             data = 0

         cursor.close()
         db.close()
         return data

#==============================================================================
#   function: get_vip
#   description: gets the view VIP
#   returns: all the vip
#==============================================================================
    def get_vip(self):
         db = MySQLdb.connect(host=self.host,
                             user=self.user,
                             passwd=self.pw,
                             db=self.db)

         get_vip_query = """SELECT * FROM VIP"""
         cursor = db.cursor()
         try:
             dataList = []
             cursor.execute(get_vip_query)
             vips = cursor.fetchall()
             for v in vips:
                 vip = {
                    'id': v[0],
                    'name': v[1],
                    'age': v[2],
                    'email': v[3],
                    'phone': v[4]
                 }
                 dataList.append(vip)
             data = json.dumps(dataList, sort_keys=True, indent=4, separators=(',', ': '))
         except Exception as err:
             data = ("Get VIP Failed with error: {0}").format(err)
             db.rollback()
             print(data)

         cursor.close()
         db.close()
         return data

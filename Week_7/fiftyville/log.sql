-- Keep a log of any SQL queries you execute as you solve the mystery.
SELECT * FROM airports; --'from CSF id = 8
SELECT * FROM flights WHERE origin_airport_id = 8 AND day >= 28;
SELECT * from crime_scene_reports WHERE ((month = 7 AND day >= 28) OR month >= 8) AND street = 'Humphrey Street'; --' to get crime date
SELECT * FROM interviews WHERE day = 28 AND month = 7; --'interviews in that day
--' crime at 2021/7/28 10:15am
--' car park alot in bakery parking
--'Sometime within ten minutes of the theft, I saw the thief get into a car in the bakery parking lot and drive away. If you have security footage from the bakery parking lot, you might want to look for cars that left the parking lot in that time frame.
--' atm at Leggett Street
--'I don't know the thief's name, but it was someone I recognized. Earlier this morning, before I arrived at Emma's bakery, I was walking by the ATM on Leggett Street and saw the thief there withdrawing some money.
--' flight at 29 cal with less that min
--' As the thief was leaving the bakery, they called someone who talked to them for less than a minute. In the call, I heard the thief say that they were planning to take the earliest flight out of Fiftyville tomorrow. The thief then asked the person on the other end of the phone to purchase the flight ticket.


SELECT caller FROM phone_calls WHERE month = 7 AND day = 28 AND duration < 60; --'his phone num is one of it

SELECT name FROM people WHERE phone_number in (SELECT caller FROM phone_calls WHERE month = 7 AND day = 28 AND duration < 60); --'name of callers


CREATE TABLE sus_phones (
  name VARCHAR(50)
);

INSERT INTO sus_phones (name)
SELECT name FROM people WHERE phone_number IN (
  SELECT caller FROM phone_calls WHERE month = 7 AND day = 28 AND duration < 60
); --'tabble for sus peopple phone number

SELECT account_number FROM atm_transactions WHERE day is 28 AND month is 7 AND atm_location is 'Leggett Street' AND transaction_type = 'withdraw';
SELECT person_id FROM bank_accounts WHERE account_number in (SELECT account_number FROM atm_transactions WHERE day is 28 AND month is 7 AND atm_location is 'Leggett Street' AND transaction_type = 'withdraw');
SELECT name FROM people WHERE id in (SELECT person_id FROM bank_accounts WHERE account_number in (SELECT account_number FROM atm_transactions WHERE day is 28 AND month is 7 AND atm_location is 'Leggett Street' AND transaction_type = 'withdraw'));
--'get list of people of been withdrawing many this day


CREATE TABLE sus_atm (
  name VARCHAR(50)
);

INSERT INTO sus_atm (name)
SELECT name FROM people WHERE id in
    (SELECT person_id FROM bank_accounts WHERE account_number in
        (SELECT account_number FROM atm_transactions WHERE day is 28 AND month is 7 AND atm_location is 'Leggett Street' AND transaction_type = 'withdraw'))
;--' creat table for sus of atm

SELECT * FROM sus_atm WHERE name in (SELECT name FROM sus_phones); --' same at phone and atm

SELECT * FROM bakery_security_logs WHERE day = 28 AND month = 7 AND activity = 'exit' AND hour >= 10 AND hour <= 11; --'people exit parking

CREATE TABLE sus_park (
  name VARCHAR(50)
);

INSERT INTO sus_park (name)
SELECT name FROM people WHERE license_plate in (SELECT license_plate FROM bakery_security_logs WHERE day = 28 AND month = 7 AND activity = 'exit' AND hour >= 10 AND hour <= 11);
--'creat table for sus from parking
SELECT name FROM sus_park WHERE name in (SELECT * FROM sus_atm WHERE name in (SELECT name FROM sus_phones));
--' he is one of Taylor Diana Bruce

SELECT * FROM flights WHERE origin_airport_id = 8 AND month = 7 AND day = 29 ORDER BY hour;
--'id of fligh is 36
SELECT name FROM people WHERE passport_number in (SELECT passport_number FROM passengers WHERE flight_id = 36);
--'people in that flight
--'Taylor Bruce

SELECT name from people where phone_number is (SELECT receiver FROM phone_calls WHERE caller is (SELECT phone_number FROM people WHERE name is 'Taylor') AND day is 28 AND duration < 60 AND month is 7);
--'Taylor > James  Bruce > Robin
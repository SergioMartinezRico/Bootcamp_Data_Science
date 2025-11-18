SELECT * 
FROM crime_scene_report
WHERE date = '20180115' AND TYPE = 'murder' AND city = 'SQL City'

-- Security footage shows that there were 2 witnesses. The first witness lives at the last house on "Northwestern Dr". The second witness, named Annabel, lives somewhere on "Franklin Ave".

SELECT id, name, address_street_name
FROM person
WHERE address_street_name = 'Northwestern Dr'
ORDER BY address_number DESC
LIMIT 1;

--id 14887

-- name Morty Schapiro

--address_street_nam Northwestern Dr


SELECT id, name, address_street_name
FROM person
WHERE name LIKE 'Annabel%' and address_street_name = 'Franklin Ave'

--id 16371

--name Annabel Miller

--address_street_name Franklin Ave

--ssn 318771143

select transcript 
from interview
where person_id = '14887'


--I heard a gunshot and then saw a man run out. He had a "Get Fit Now Gym" bag. The membership number on the bag --started with "48Z". Only gold members have those bags. The man got into a car with a plate that included "H42W".

select transcript 
from interview
where person_id = '16371'

--I saw the murder happen, and I recognized the killer from my gym when I was working out last week on January the 9th.

select *
from get_fit_now_member
where id like '48Z%' and membership_status ='gold'

--48Z55
--person_id 67318
--name Jeremy Bowers
--membership_start_date 20160101
--membership_status gold



--id 48Z7A
--person_id 28819
--name Joe Germuska
--membership_start_date 20160305
--membership_status gold

SELECT p.id, p.name, dl.plate_number
FROM person AS p
JOIN drivers_license AS dl
ON p.license_id = dl.id
WHERE p.id IN (67318, 28819) 
AND dl.plate_number LIKE '%H42W%'

--Jeremy Bowers es el asesino
CREATE SCHEMA hive.s3 WITH (location='s3a://reactions239-development/test');

CREATE TABLE hive.s3.people (
                        age INTEGER,
                        name ROW (
                            given varchar,
                            family varchar )
                       ) WITH (
                        format='JSON'
                       );

INSERT INTO hive.s3.people VALUES (43, ('Owain', 'Kenway'));

SELECT * FROM hive.s3.people;

DROP TABLE hive.s3.people;
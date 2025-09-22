CREATE SCHEMA hive.reactions WITH (
    location='{uri}/reactions'
    );

CREATE TABLE hive.reactions.reactions (
    reactants ARRAY (
        ROW (
            C INTEGER,
            H INTEGER,
            N INTEGER,
            O INTEGER
        )),
    products ARRAY (
        ROW (
            C INTEGER,
            H INTEGER,
            N INTEGER,
            O INTEGER
        )))
    WITH (
        format='JSON',
        external_location = '{uri}/reactions/reactions'
    )
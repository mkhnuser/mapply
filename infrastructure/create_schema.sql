CREATE TABLE map_events(
    id SERIAL PRIMARY KEY,
    title VARCHAR(64) NOT NULL,
    description VARCHAR(512) NOT NULL,
    lat REAL NOT NULL CHECK (lat >= -90 AND lat <= 90),
    lng REAL NOT NULL CHECK (lng >= -180 AND lng <= 180)
);

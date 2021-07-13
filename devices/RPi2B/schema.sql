BEGIN TRANSACTION;

CREATE TABLE sensors (
    id INTEGER NOT NULL PRIMARY KEY,
    name TEXT NOT NULL UNIQUE,
    details TEXT
);

INSERT INTO sensors(id, name, details) VALUES (1, 'ZJZ Izba', 'Raspberry Pi 2B, Wifi dongle, DS18B20 (teplota) 5m');
INSERT INTO sensors(id, name, details) VALUES (2, 'JJV Izba', 'Wemos D1 Mini Pro ESP8266, DHT22 (teplota, vlhkosť), Fotorezistor LDR5516 (svetlo), Batérie 4xAA NiMH 1.2V 2100 mAh Ansman MaxE, Solárny panel');
INSERT INTO sensors(id, name, details) VALUES (3, 'ZJZ Presklenný balkón', 'Lolin ESP8266, BMP280 (teplota, tlak), Fotodióda SFH203 (svetlo), Batérie 4xAA NiMH 1.2V 1900 mAh Enelope');


CREATE TABLE measurements (
    id INTEGER NOT NULL PRIMARY KEY,
    sensor_id INTEGER NOT NULL REFERENCES sensors(id),
    measured_at DATETIME NOT NULL DEFAULT (datetime('now', 'localtime')),
    t_celsius DECIMAL(5, 2),
    light_analog INTEGER,                  
    p_mslp_pa INTEGER,
    rel_humidity INTEGER
);

CREATE TABLE openweathermap(
    id INTEGER NOT NULL PRIMARY KEY,
    reference_time DATETIME, 
    sunrise_time DATETIME, 
    sunset_time DATETIME,
    clouds INTEGER,
    rain INTEGER,
    wind_speed DECIMAL(5, 2),
    wind_deg INTEGER,
    humidity INTEGER, 
    pressure INTEGER,
    temperature DECIMAL(5, 2),
    status TEXT, 
    detailed_status TEXT,
    weather_code INT,
    visibility_distance INT
);

COMMIT;

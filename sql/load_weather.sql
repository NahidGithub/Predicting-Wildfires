

DROP TABLE IF EXISTS weather_loading_pk;
CREATE TABLE weather_loading_pk AS (
SELECT CONCAT(latitude,"|",longitude,"|",YEAR(timestamp),"|",DAYOFYEAR(timestamp)) pk, w.*
FROM weather_loading w
GROUP BY pk);

DROP TABLE IF EXISTS nasa_emissions_doycombined_May28_pk;
CREATE TABLE nasa_emissions_doycombined_May28_pk AS (
SELECT CONCAT(latitude,"|",longitude,"|",`year`,"|",cluster_doy) pk, w.*
FROM nasa_emissions_doycombined_May28 w
GROUP BY pk);

-- MAKE SURE TO ACTUALLY SET THE PK IN THE TABLES YOU WERE TOO LAZY TO DO IT IN CODE


TRUNCATE db65uftgqqttp3.Weather;
INSERT INTO db65uftgqqttp3.Weather
SELECT NULL `Key`,
	COALESCE(cluster_reference,'unknown') cluster_ref,
	w.latitude lat,
	w.longitude lon,
	apparentTemperature temperature,
	humidity,
	precipIntensity precip_intensity,
	pressure,
	uvIndex ux_index,
	visibility,
	windSpeed wind_speed,
	windGust wind_gust,
	timestamp Date,
	YEAR(timestamp) weather_year,
	DAYOFYEAR(timestamp) doy
from db27bvsdruzh45.weather_loading_pk w
LEFT OUTER JOIN db27bvsdruzh45.nasa_emissions_doycombined_May28_pk c
	 on c.pk = w.pk
GROUP BY w.latitude, w.longitude, year, cluster_doy, cluster_reference
;


ANALYZE TABLE db65uftgqqttp3.Weather;
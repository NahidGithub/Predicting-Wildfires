TRUNCATE db65uftgqqttp3.NASA;
INSERT INTO db65uftgqqttp3.NASA
select NULL `Key`,
	COALESCE(target_clusterref, 'unknown') cluster_ref,
	latitude lat,
	longitude lon,
	brightness,
	acq_date,
	acq_time,
	bright_t31,
	frp,
	daynight,
	YEAR(acq_date) year,
	DAYOFYEAR(acq_date) doy
from `nasa_cluster_match`
;


ANALYZE TABLE db65uftgqqttp3.NASA;
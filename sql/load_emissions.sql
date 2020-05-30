TRUNCATE db65uftgqqttp3.Emissions_Data;
INSERT INTO db65uftgqqttp3.Emissions_Data
select NULL `Key`,
	id,
	COALESCE(cluster_reference,'unknown') cluster_ref,
	longitude lon,
	latitude lat,
	year,
	doy,
	covertype,
	fuelcode,
	prefire_fuel,
	consumed_fuel,
	ECO2,
	ECO,
	ECH4,
	`EPM2.5`,
	fuel_moisture_class,
	BSEV,
	cwd_frac,
	duff_frac
 
from `emissions_03_15_v5.24`
;


ANALYZE TABLE db65uftgqqttp3.Emissions_Data;
CREATE TABLE `Weather` (
	`Key` int NOT NULL AUTO_INCREMENT,
	`cluster_ref` VARCHAR(50) NOT NULL,
	`lat` double NOT NULL,
	`lon` double NOT NULL,
	`temperature` double NOT NULL,
	`humidity` double,
	`precip_intensity` double NOT NULL,
	`pressure` double NOT NULL,
	`uvIndex` double NOT NULL,
	`visibility` double NOT NULL,
	`wind_speed` double NOT NULL,
	`wind_gust` double NOT NULL,
	`Date` TIMESTAMP NOT NULL,
	PRIMARY KEY (`Key`)
);

CREATE TABLE `Fire_Table` (
	`cluster_ref` VARCHAR(50) NOT NULL UNIQUE,
	`lat` double NOT NULL,
	`lon` double NOT NULL,
	`fire_name` VARCHAR(255) NOT NULL,
	`discovery_doy` int NOT NULL,
	`contain_doy` int NOT NULL,
	`duration` int NOT NULL,
	`year` int NOT NULL,
	`doy` int NOT NULL,
	`fire_size` double NOT NULL,
	`fire_class` int NOT NULL,
	`BSEV` int NOT NULL,
	`max_fire_radiation` double NOT NULL,
	`max_emission_output` double NOT NULL,
	`altitude` int NOT NULL,
	PRIMARY KEY (`cluster_ref`)
);

CREATE TABLE `NASA` (
	`Key` int NOT NULL AUTO_INCREMENT,
	`cluster_ref` VARCHAR(50) NOT NULL,
	`lat` double NOT NULL,
	`lon` double NOT NULL,
	`brightness` double NOT NULL,
	`acq_date` TIMESTAMP NOT NULL,
	`acq_time` time NOT NULL,
	`bright_t31` double NOT NULL,
	`frp` double NOT NULL,
	`daynight` VARCHAR(50) NOT NULL,
	`year` int NOT NULL,
	`doy` int NOT NULL,
	PRIMARY KEY (`Key`)
);

CREATE TABLE `Emissions_Data` (
	`Key` int NOT NULL AUTO_INCREMENT,
	`id` int NOT NULL,
	`cluster_ref` VARCHAR(50) NOT NULL,
	`lon` double NOT NULL,
	`lat` double NOT NULL,
	`year` int NOT NULL,
	`doy` int NOT NULL,
	`covertype` int NOT NULL,
	`fuelcode` int NOT NULL,
	`prefire_fuel` double NOT NULL,
	`consumed_fuel` double NOT NULL,
	`ECO2` double NOT NULL,
	`ECO` double NOT NULL,
	`ECH4` double NOT NULL,
	`EPM2.5` double NOT NULL,
	`fuel_moisture_class` double NOT NULL,
	`BSEV` double NOT NULL,
	`cwd_frac` double NOT NULL,
	`duff_frac` double NOT NULL,
	PRIMARY KEY (`Key`)
);

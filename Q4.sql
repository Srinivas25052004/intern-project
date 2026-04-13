CREATE TABLE capacity_stability_2025 AS
SELECT 
    MachineID,
    Plant,
    AVG(ProductionUnits) AS AvgOutput,
    STDDEV(ProductionUnits) AS StdOutput,
    STDDEV(ProductionUnits) / AVG(ProductionUnits) AS CV_Output,
    SUM(CASE WHEN MaintenanceFlag = 1 THEN 1 ELSE 0 END) AS MaintenanceCount,
    SUM(DefectCount) AS DefectCountTotal
FROM production_data
GROUP BY MachineID, Plant;

USE production_db;

CREATE TABLE capacity_stability_2025 AS
SELECT 
    MachineID,
    Plant,
    AVG(ProductionUnits) AS AvgOutput,
    STDDEV(ProductionUnits) AS StdOutput,
    STDDEV(ProductionUnits) / AVG(ProductionUnits) AS CV_Output,
    SUM(CASE WHEN MaintenanceFlag = 1 THEN 1 ELSE 0 END) AS MaintenanceCount,
    0 AS DefectCountTotal
FROM production_data
GROUP BY MachineID, Plant;

DESCRIBE production_data;

DROP TABLE capacity_stability_2025;


CREATE TABLE capacity_stability_2025 (
    MachineID VARCHAR(50),
    Plant VARCHAR(50),
    AvgOutput DECIMAL(10,2),
    StdOutput DECIMAL(10,2),
    CV_Output DECIMAL(10,4),
    MaintenanceCount INT,
    DefectCountTotal INT
);


INSERT INTO capacity_stability_2025
SELECT 
    MachineID,
    Plant,
    AVG(ProductionUnits),
    STDDEV(ProductionUnits),
    STDDEV(ProductionUnits) / AVG(ProductionUnits),
    SUM(CASE WHEN MaintenanceFlag = 1 THEN 1 ELSE 0 END),
    SUM(DefectCount)
FROM production_data
GROUP BY MachineID, Plant;

DROP TABLE capacity_stability_2025;

CREATE TABLE capacity_stability_2025 (
    MachineID VARCHAR(50),
    Plant VARCHAR(50),
    AvgOutput DECIMAL(15,4),
    StdOutput DECIMAL(15,4),
    CV_Output DECIMAL(15,6),
    MaintenanceCount INT,
    DefectCountTotal INT
);

INSERT INTO capacity_stability_2025
SELECT 
    MachineID,
    Plant,
    AVG(ProductionUnits),
    STDDEV(ProductionUnits),
    STDDEV(ProductionUnits) / AVG(ProductionUnits),
    SUM(CASE WHEN MaintenanceFlag = 1 THEN 1 ELSE 0 END),
    SUM(DefectCount)
FROM production_data
GROUP BY MachineID, Plant;


DROP TABLE capacity_stability_2025;

CREATE TABLE capacity_stability_2025 (
    MachineID VARCHAR(50),
    Plant VARCHAR(50),
    AvgOutput DOUBLE,
    StdOutput DOUBLE,
    CV_Output DOUBLE,
    MaintenanceCount INT,
    DefectCountTotal INT
);

INSERT INTO capacity_stability_2025 
(MachineID, Plant, AvgOutput, StdOutput, CV_Output, MaintenanceCount, DefectCountTotal)
SELECT 
    MachineID,
    Plant,
    AVG(ProductionUnits),
    STDDEV(ProductionUnits),
    STDDEV(ProductionUnits) / AVG(ProductionUnits),
    SUM(CASE WHEN MaintenanceFlag = 1 THEN 1 ELSE 0 END),
    SUM(DefectCount)
FROM production_data
GROUP BY MachineID, Plant;

SELECT * FROM capacity_stability_2025 LIMIT 10;

USE production_db;

SELECT * FROM capacity_stability_2025 LIMIT 10;
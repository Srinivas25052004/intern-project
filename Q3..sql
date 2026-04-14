


USE production_db;


SELECT 
    MachineID,
    Plant,
    AVG(ProductionUnits) AS AvgProduction,
    COUNT(CASE WHEN MaintenanceFlag = 1 THEN 1 END) AS MaintenanceCount
FROM production_data
GROUP BY MachineID, Plant
ORDER BY AvgProduction ASC
LIMIT 10;
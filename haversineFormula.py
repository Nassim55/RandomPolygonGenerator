import math

def haversineFormula(latRadians1, latRadians2, longRadians1, longRadians2):
    earthRadiusMeters = 6371000

    latRadians1 = math.radians(latRadians1)
    latRadians2 = math.radians(latRadians2)
    longRadians1 = math.radians(longRadians1)
    longRadians2 = math.radians(longRadians2)

    deltaLat = latRadians2 - latRadians1 
    deltaLong = longRadians2 - longRadians1

    constA = (math.sin(deltaLat / 2) * math.sin(deltaLat / 2)) + (math.cos(latRadians1) * math.cos(latRadians2) * math.sin(deltaLong / 2) * math.sin(deltaLong / 2))
    constC = 2 * math.atan2(math.sqrt(constA), math.sqrt(1-constA))
    constD = earthRadiusMeters * constC

    return constD
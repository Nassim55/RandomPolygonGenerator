import math
import random
import matplotlib.pyplot as plt
from haversineFormula import haversineFormula

# For use in haversine formula:
earthRadiusMeters = 6371000

# Users location:
original_longitude = -1.55459
original_latitude = 55.0198

# Route distance, will be input by user:
routeDistanceMeters = 2000

# Polygon parameters:
numberOfPoints = 20
radiusMeters = routeDistanceMeters / (2 * math.pi)
radiusDegrees = radiusMeters / 111300
print(radiusDegrees)
deltaTheta = (2 * math.pi) / (numberOfPoints - 1)

# Generating a random circle and random:
thetaIncrements = 0
perimeterIncrements = 0
coordsPolygon = []
randomRadiusLst = []
for i in range(numberOfPoints):
    if i == (numberOfPoints - 1):
        randomRadiusLst.append(randomRadiusLst[0])
        coordsPolygon.append(coordsPolygon[0])
        distanceBetweenCoords = haversineFormula(coordsPolygon[i-1][1], coordsPolygon[i][1], coordsPolygon[i-1][0], coordsPolygon[i][0])
        perimeterIncrements += distanceBetweenCoords
    else:
        randomRadiusDegrees = radiusDegrees - random.uniform(0, (0.8 * radiusDegrees))
        randomRadiusLst.append(randomRadiusDegrees)
        xCoord = randomRadiusDegrees * math.cos(thetaIncrements)
        yCoord = randomRadiusDegrees * math.sin(thetaIncrements)
        X = (xCoord + original_longitude) / math.cos(math.radians(original_latitude))
        Y = yCoord + original_latitude
        coordsPolygon.append([X, Y])
        thetaIncrements += deltaTheta

        distanceBetweenCoords = haversineFormula(coordsPolygon[i-1][1], coordsPolygon[i][1], coordsPolygon[i-1][0], coordsPolygon[i][0])
        perimeterIncrements += distanceBetweenCoords

print(perimeterIncrements)

scalingRatio = 0.01
if perimeterIncrements > routeDistanceMeters:
    while perimeterIncrements > routeDistanceMeters:
        print(perimeterIncrements)
        thetaIncrements = 0
        iteratePerimeterIncrements = 0
        for i in range(len(coordsPolygon)):
            randomRadiusLst[i] = randomRadiusLst[i] * (1 - scalingRatio)
            coordsPolygon[i][0] = ((randomRadiusLst[i] * math.cos(thetaIncrements)) + original_longitude) / math.cos(math.radians(original_latitude))
            coordsPolygon[i][1] = (randomRadiusLst[i] * math.sin(thetaIncrements)) + original_latitude
            thetaIncrements += deltaTheta
            distanceBetweenCoords = haversineFormula(coordsPolygon[i-1][1], coordsPolygon[i][1], coordsPolygon[i-1][0], coordsPolygon[i][0])
            iteratePerimeterIncrements += distanceBetweenCoords
        perimeterIncrements = iteratePerimeterIncrements
else:
    while perimeterIncrements < routeDistanceMeters:
        print(perimeterIncrements)
        thetaIncrements = 0
        iteratePerimeterIncrements = 0
        for i in range(len(coordsPolygon)):
            randomRadiusLst[i] = randomRadiusLst[i] * (1 + scalingRatio)
            coordsPolygon[i][0] = ((randomRadiusLst[i] * math.cos(thetaIncrements)) + original_longitude) / math.cos(math.radians(original_latitude))
            coordsPolygon[i][1] = (randomRadiusLst[i] * math.sin(thetaIncrements)) + original_latitude
            thetaIncrements += deltaTheta
            distanceBetweenCoords = haversineFormula(coordsPolygon[i-1][1], coordsPolygon[i][1], coordsPolygon[i-1][0], coordsPolygon[i][0])
            iteratePerimeterIncrements += distanceBetweenCoords
        perimeterIncrements = iteratePerimeterIncrements



longDifference =  coordsPolygon[0][0] - original_longitude
for i in range(len(coordsPolygon)-1):
    coordsPolygon[i][0] = coordsPolygon[i][0] - longDifference
print(coordsPolygon)
print(perimeterIncrements)

X_coordsPolygon = [i[0] for i in coordsPolygon]
Y_coordsPolygon = [i[1] for i in coordsPolygon]

plt.plot(X_coordsPolygon, Y_coordsPolygon, linestyle='--', marker='o', color='b')
plt.plot(X_coordsPolygon[0], Y_coordsPolygon[0], linestyle='--', marker='o', color='r')
plt.grid()
plt.show()
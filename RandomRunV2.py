import math
import random
import matplotlib.pyplot as plt

# Users location:
original_longitude = -1.55459
original_latitude = 55.0198

# Route distance, will be input by user:
routeDistanceMeters = 2000

# Polygon parameters:
numberOfPoints = 20
radiusMeters = routeDistanceMeters / (2 * math.pi)
radiusDegrees = radiusMeters / 111300
deltaTheta = (2 * math.pi) / (numberOfPoints - 1)

# Generating a random circle and random:
thetaIncrements = 0
coordsPolygon = []
for i in range (numberOfPoints):
    xCoord = radiusDegrees * math.cos(thetaIncrements)
    yCoord = radiusDegrees * math.sin(thetaIncrements)
    X = (xCoord + original_longitude) / math.cos(math.radians(original_latitude))
    Y = yCoord + original_latitude

    coordsPolygon.append([X, Y])

    thetaIncrements += deltaTheta






X_coordsPolygon = [i[0] for i in coordsPolygon]
Y_coordsPolygon = [i[1] for i in coordsPolygon]

print(X_coordsPolygon)
print(Y_coordsPolygon)

plt.plot(X_coordsPolygon, Y_coordsPolygon, linestyle='--', marker='o', color='b')
plt.plot(X_coordsPolygon[0], Y_coordsPolygon[0], linestyle='--', marker='o', color='r')
plt.grid()
plt.show()
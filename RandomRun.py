import math
import random
import matplotlib.pyplot as plt

original_longitude = -1.55459
original_latitude = 55.0198
numberOfEdges = 20  # Number of edges on polygon
radius =  1  # Radius (polar co-ordinates)
deltaTheta = (2 * math.pi) / numberOfEdges  # Change in angle per point (polar co-ordinates)
routeDistanceMeters = 2000
routeDistanceDegrees = routeDistanceMeters / 111300
routeDistanceRadian = math.radians(routeDistanceDegrees)
radiusMeters = routeDistanceMeters / (2 * math.pi)
print('route distance meters: ' + str(routeDistanceMeters))
perimeter = 2 * math.pi * radiusMeters

east_west_scaling = math.cos(math.radians(original_latitude))

# For each delta theta defining a list of X and Y co-ordinates for the unit circle polygon and
# generating a random polygon by varying the radius  
currentTheta = 0
coordsPolygon = [[1, 0]] 
coordsRandomPolygon = [[1, 0]]
perimeterPolygon = 0
perimeterRandomPolygon = 0
randomRadiusLst = []
for i in range(numberOfEdges):    
    currentTheta += deltaTheta
    randomRadius = radius - random.uniform(0, (0.8 * radiusMeters))
    randomRadiusLst.append(randomRadius)

    if (i ==  (numberOfEdges - 1)):
        coordsPolygon.append([1, 0])
        coordsRandomPolygon.append([1, 0])
    else:
        coordsPolygon.append([radiusMeters * math.cos(currentTheta), radiusMeters * math.sin(currentTheta)])
        coordsRandomPolygon.append([randomRadius * math.cos(currentTheta), randomRadius * math.sin(currentTheta)])

    # Distance between points for unit circle polygon and random polygon 
    perimeterPolygon += math.sqrt((coordsPolygon[i][0]-coordsPolygon[i-1][0])**2 + (coordsPolygon[i][1]-coordsPolygon[i-1][1])**2) 
    perimeterRandomPolygon += math.sqrt((coordsRandomPolygon[i][0]-coordsRandomPolygon[i-1][0])**2 + (coordsRandomPolygon[i][1]-coordsRandomPolygon[i-1][1])**2)

print('perimeter of random polygon: ' + str(perimeterRandomPolygon))

# Scaling the random polygon to the perimeter of the original unit circle
scalingFactor = routeDistanceMeters / perimeterRandomPolygon
print(scalingFactor)
currentTheta = 0
coordsRandomPolygonScaled = [[((1 * scalingFactor) * math.cos(currentTheta)), (0 * scalingFactor) * math.sin(currentTheta)]]
perimeterScaledRandomPolygon = 0
for i in range(numberOfEdges):
    currentTheta += deltaTheta
    if (i ==  (numberOfEdges - 1)):
        coordsRandomPolygonScaled.append([((1 * scalingFactor) * math.cos(currentTheta)), (0 * scalingFactor) * math.sin(currentTheta)])
    else:
        coordsRandomPolygonScaled.append([((randomRadiusLst[i] * scalingFactor) * math.cos(currentTheta)), (randomRadiusLst[i] * scalingFactor) * math.sin(currentTheta)])

    perimeterScaledRandomPolygon += math.sqrt((coordsRandomPolygonScaled[i][0]-coordsRandomPolygonScaled[i-1][0])**2 + (coordsRandomPolygonScaled[i][1]-coordsRandomPolygonScaled[i-1][1])**2)

for i in range(len(coordsRandomPolygonScaled)):
    coordsRandomPolygonScaled[i][0] = coordsRandomPolygonScaled[i][0] / east_west_scaling

if perimeterScaledRandomPolygon > routeDistanceRadian:
    while perimeterScaledRandomPolygon > perimeter:
        scalingFactor = scalingFactor - (scalingFactor * (0.3))
        currentTheta = 0
        coordsRandomPolygonScaled = [[(1 * scalingFactor) * math.cos(currentTheta), (0 * scalingFactor) * math.sin(currentTheta)]]
        iteratePerimeterScaledRandomPolygon = 0
        for i in range(numberOfEdges):
            currentTheta += deltaTheta
            if (i ==  (numberOfEdges - 1)):
                coordsRandomPolygonScaled.append([(1 * scalingFactor) * math.cos(currentTheta), (0 * scalingFactor) * math.sin(currentTheta)])
            else:
                coordsRandomPolygonScaled.append([(randomRadiusLst[i] * scalingFactor) * math.cos(currentTheta), (randomRadiusLst[i] * scalingFactor) * math.sin(currentTheta)])

            iteratePerimeterScaledRandomPolygon += math.sqrt((coordsRandomPolygonScaled[i][0]-coordsRandomPolygonScaled[i-1][0])**2 + (coordsRandomPolygonScaled[i][1]-coordsRandomPolygonScaled[i-1][1])**2)
        perimeterScaledRandomPolygon = iteratePerimeterScaledRandomPolygon
else:
    while perimeterScaledRandomPolygon > routeDistanceRadian:
        scalingFactor = scalingFactor + (scalingFactor * (0.3))
        currentTheta = 0
        coordsRandomPolygonScaled = [[(1 * scalingFactor) * math.cos(currentTheta), (0 * scalingFactor) * math.sin(currentTheta)]]
        iteratePerimeterScaledRandomPolygon = 0
        for i in range(numberOfEdges):
            currentTheta += deltaTheta
            if (i ==  (numberOfEdges - 1)):
                coordsRandomPolygonScaled.append([(1 * scalingFactor) * math.cos(currentTheta), (0 * scalingFactor) * math.sin(currentTheta)])
            else:
                coordsRandomPolygonScaled.append([(randomRadiusLst[i] * scalingFactor) * math.cos(currentTheta), (randomRadiusLst[i] * scalingFactor) * math.sin(currentTheta)])

            iteratePerimeterScaledRandomPolygon += math.sqrt((coordsRandomPolygonScaled[i][0]-coordsRandomPolygonScaled[i-1][0])**2 + (coordsRandomPolygonScaled[i][1]-coordsRandomPolygonScaled[i-1][1])**2)
        perimeterScaledRandomPolygon = iteratePerimeterScaledRandomPolygon


originXScaledRandomPolygon = coordsRandomPolygonScaled[0][0]
originYScaledRandomPolygon = coordsRandomPolygonScaled[0][1]
translatedRouteCoords = []
for coord in coordsRandomPolygonScaled:
    translatedRouteCoords.append([(coord[0]-originXScaledRandomPolygon), coord[1]])

print('Scaled Random Polygon Perimeter: ' + str(perimeterScaledRandomPolygon))



#X_coordsPolygon = [(i[0] + original_longitude) for i in coordsPolygon]
#Y_coordsPolygon = [(i[1] + original_latitude) for i in coordsPolygon]
#X_coordsRandomPolygon = [(i[0] + original_longitude) for i in coordsRandomPolygon]
#Y_coordsRandomPolygon = [(i[1] + original_latitude) for i in coordsRandomPolygon]
#X_coordsRandomPolygonScaled = [(i[0] + original_longitude) for i in coordsRandomPolygonScaled]
#Y_coordsRandomPolygonScaled = [(i[1] + original_latitude) for i in coordsRandomPolygonScaled]
#X_translatedRouteCoords = [(i[0] + original_longitude) for i in translatedRouteCoords]
#Y_translatedRouteCoords = [(i[1] + original_latitude) for i in translatedRouteCoords]



#X_coordsPolygon = [i[0] for i in coordsPolygon]
#Y_coordsPolygon = [i[1] for i in coordsPolygon]
#X_coordsRandomPolygon = [i[0] for i in coordsRandomPolygon]
#Y_coordsRandomPolygon = [i[1] for i in coordsRandomPolygon]
#X_coordsRandomPolygonScaled = [i[0] for i in coordsRandomPolygonScaled]
#Y_coordsRandomPolygonScaled = [i[1] for i in coordsRandomPolygonScaled]
X_translatedRouteCoords = [i[0] for i in translatedRouteCoords]
Y_translatedRouteCoords = [i[1] for i in translatedRouteCoords]


#plt.plot(X_coordsPolygon, Y_coordsPolygon, linestyle='--', marker='o', color='y')
#plt.plot(X_coordsPolygon[0], Y_coordsPolygon[0], linestyle='--', marker='o', color='r')
#plt.plot(X_coordsRandomPolygon, Y_coordsRandomPolygon, linestyle='--', marker='o', color='b')
#plt.plot(X_coordsRandomPolygon[0], Y_coordsRandomPolygon[0], linestyle='--', marker='o', color='r')
#plt.plot(X_coordsRandomPolygonScaled, Y_coordsRandomPolygonScaled, linestyle='--', marker='o', color='g')
#plt.plot(X_coordsRandomPolygonScaled[0], Y_coordsRandomPolygonScaled[0],  linestyle='--', marker='o', color='r')

plt.plot(X_translatedRouteCoords, Y_translatedRouteCoords, linestyle='--', marker='o', color='b')
plt.plot(X_translatedRouteCoords[0], Y_translatedRouteCoords[0],  linestyle='--', marker='o', color='r')
plt.grid()
plt.show()




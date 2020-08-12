import math
import random
import matplotlib.pyplot as plt


numberOfEdges = 20  # Number of edges on polygon
radius =  1  # Radius (polar co-ordinates)
deltaTheta = (2 * math.pi) / numberOfEdges  # Change in angle per point (polar co-ordinates)
perimeter = 2 * math.pi * radius

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
    randomRadius = radius - random.uniform(0, (0.8 * radius))
    randomRadiusLst.append(randomRadius)

    if (i ==  (numberOfEdges - 1)):
        coordsPolygon.append([1, 0])
        coordsRandomPolygon.append([1, 0])
    else:
        coordsPolygon.append([radius * math.cos(currentTheta), radius * math.sin(currentTheta)])
        coordsRandomPolygon.append([randomRadius * math.cos(currentTheta), randomRadius * math.sin(currentTheta)])

    # Distance between points for unit circle polygon and random polygon 
    perimeterPolygon += math.sqrt((coordsPolygon[i][0]-coordsPolygon[i-1][0])**2 + (coordsPolygon[i][1]-coordsPolygon[i-1][1])**2) 
    perimeterRandomPolygon += math.sqrt((coordsRandomPolygon[i][0]-coordsRandomPolygon[i-1][0])**2 + (coordsRandomPolygon[i][1]-coordsRandomPolygon[i-1][1])**2)


# Scaling the random polygon to the perimeter of the original unit circle
scalingFactor = perimeter / perimeterRandomPolygon
currentTheta = 0
coordsRandomPolygonScaled = [[1, 0]]
perimeterScaledRandomPolygon = 0
for i in range(numberOfEdges):
    currentTheta += deltaTheta
    if (i ==  (numberOfEdges - 1)):
        coordsRandomPolygonScaled.append([1, 0])
    else:
        coordsRandomPolygonScaled.append([(randomRadiusLst[i] * scalingFactor) * math.cos(currentTheta), (randomRadiusLst[i] * scalingFactor) * math.sin(currentTheta)])

    perimeterScaledRandomPolygon += math.sqrt((coordsRandomPolygonScaled[i][0]-coordsRandomPolygonScaled[i-1][0])**2 + (coordsRandomPolygonScaled[i][1]-coordsRandomPolygonScaled[i-1][1])**2)

print(scalingFactor)

if perimeterScaledRandomPolygon > perimeter:
    while perimeterScaledRandomPolygon > perimeter:
        scalingFactor = scalingFactor - (scalingFactor * (0.00001))
        currentTheta = 0
        coordsRandomPolygonScaled = [[1, 0]]
        iteratePerimeterScaledRandomPolygon = 0
        for i in range(numberOfEdges):
            currentTheta += deltaTheta
            if (i ==  (numberOfEdges - 1)):
                coordsRandomPolygonScaled.append([1, 0])
            else:
                coordsRandomPolygonScaled.append([(randomRadiusLst[i] * scalingFactor) * math.cos(currentTheta), (randomRadiusLst[i] * scalingFactor) * math.sin(currentTheta)])

            iteratePerimeterScaledRandomPolygon += math.sqrt((coordsRandomPolygonScaled[i][0]-coordsRandomPolygonScaled[i-1][0])**2 + (coordsRandomPolygonScaled[i][1]-coordsRandomPolygonScaled[i-1][1])**2)
        perimeterScaledRandomPolygon = iteratePerimeterScaledRandomPolygon

if perimeterScaledRandomPolygon < perimeter:
    while perimeterScaledRandomPolygon > perimeter:
        scalingFactor = scalingFactor + (scalingFactor * (0.00001))
        currentTheta = 0
        coordsRandomPolygonScaled = [[1, 0]]
        iteratePerimeterScaledRandomPolygon = 0
        for i in range(numberOfEdges):
            currentTheta += deltaTheta
            if (i ==  (numberOfEdges - 1)):
                coordsRandomPolygonScaled.append([1, 0])
            else:
                coordsRandomPolygonScaled.append([(randomRadiusLst[i] * scalingFactor) * math.cos(currentTheta), (randomRadiusLst[i] * scalingFactor) * math.sin(currentTheta)])

            iteratePerimeterScaledRandomPolygon += math.sqrt((coordsRandomPolygonScaled[i][0]-coordsRandomPolygonScaled[i-1][0])**2 + (coordsRandomPolygonScaled[i][1]-coordsRandomPolygonScaled[i-1][1])**2)
        perimeterScaledRandomPolygon = iteratePerimeterScaledRandomPolygon




print('Perimeter: ' + str(perimeter))
print('Scaled Random Polygon Perimeter: ' + str(perimeterScaledRandomPolygon))

X_coordsPolygon = [i[0] for i in coordsPolygon]
Y_coordsPolygon = [i[1] for i in coordsPolygon]
X_coordsRandomPolygon = [i[0] for i in coordsRandomPolygon]
Y_coordsRandomPolygon = [i[1] for i in coordsRandomPolygon]
X_coordsRandomPolygonScaled = [i[0] for i in coordsRandomPolygonScaled]
Y_coordsRandomPolygonScaled = [i[1] for i in coordsRandomPolygonScaled]

plt.plot(X_coordsPolygon, Y_coordsPolygon, linestyle='--', marker='o', color='y')
plt.plot(X_coordsPolygon[0], Y_coordsPolygon[0], linestyle='--', marker='o', color='r')
plt.plot(X_coordsRandomPolygon, Y_coordsRandomPolygon, linestyle='--', marker='o', color='b')
plt.plot(X_coordsRandomPolygon[0], Y_coordsRandomPolygon[0], linestyle='--', marker='o', color='r')
plt.plot(X_coordsRandomPolygonScaled, Y_coordsRandomPolygonScaled, linestyle='--', marker='o', color='g')
plt.plot(X_coordsRandomPolygonScaled[0], Y_coordsRandomPolygonScaled[0],  linestyle='--', marker='o', color='r')
plt.grid()
plt.show()




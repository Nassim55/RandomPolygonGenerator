import math
import random
import collections
import matplotlib.pyplot as plt
from haversineFormula import haversineFormula
from settings import *
from flask import Flask, jsonify, request, Response, session
import requests

from routeBounds import routeBounds

@app.route('/route', methods=['GET'])
def getRandomRoute():
    original_longitude = float(request.args['longitude'])
    original_latitude = float(request.args['latitude'])
    routeDistanceMeters = float(request.args['routeDistance'])

    # API key:
    MAPBOX_API_KEY = 'pk.eyJ1IjoibmFzc2ltY2hlbm91ZiIsImEiOiJja2R1NjE2amMzYnl4MzByb3c5YmxlMGY5In0.cBj3YeAh0UMxinxOfhDLIw'

    # For use in haversine formula:
    earthRadiusMeters = 6371000
    
    # Polygon parameters:
    numberOfPoints = 5
    routeDistanceCorrectionFactor = 0.65
    radiusMeters = routeDistanceMeters / (2 * math.pi)
    radiusDegrees = radiusMeters / 111300
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

    scalingRatio = 0.01
    if perimeterIncrements > (routeDistanceMeters * routeDistanceCorrectionFactor):
        while perimeterIncrements > (routeDistanceMeters * routeDistanceCorrectionFactor):
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
        while perimeterIncrements < (routeDistanceMeters * routeDistanceCorrectionFactor):
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

    # Applying a random rotation to the random polygon so that all routes aren't in the same direction:
    randomRotationAngle = random.uniform(0, (2 * math.pi))
    for i in range(len(coordsPolygon)):
        # Bringing user location to origin of zero:
        coordsPolygon[i][0] -= original_longitude
        coordsPolygon[i][1] -= original_latitude
        # Applying rotation by the randomised angle:
        xRotation = (coordsPolygon[i][0] * (math.cos(randomRotationAngle))) - (coordsPolygon[i][1] * (math.sin(randomRotationAngle)))
        yRotation = (coordsPolygon[i][0] * (math.sin(randomRotationAngle))) + (coordsPolygon[i][1] * (math.cos(randomRotationAngle)))
        coordsPolygon[i][0] = xRotation
        coordsPolygon[i][1] = yRotation
        # Bringing origin back to user location:
        coordsPolygon[i][0] += original_longitude
        coordsPolygon[i][1] += original_latitude

    #Defining session variables:
    session['original_longitude'] = original_longitude
    session['original_latitude'] = original_latitude
    session['routeDistanceMeters'] = routeDistanceMeters
    session['perimeter'] = perimeterIncrements
    session['coordsPolygon'] = coordsPolygon
    session['randomRadiusLst'] = randomRadiusLst




    # Formats coords for get request:
    for i in range(len(coordsPolygon)):
        for j in range(len(coordsPolygon[i])):
            coordsPolygon[i][j] = str(coordsPolygon[i][j])
    for i in range(len(coordsPolygon)):
        coordsPolygon[i] = ','.join(coordsPolygon[i])
    coordsPolygon = ';'.join(coordsPolygon)

    response = requests.get(f'https://api.mapbox.com/directions/v5/mapbox/walking/{coordsPolygon}?alternatives=false&geometries=geojson&steps=true&continue_straight=false&access_token={MAPBOX_API_KEY}')
    data = response.json()

    originalMapboxRouteDistanceMeters = data['routes'][0]['distance']
    originalMapboxRouteCoordinates = data['routes'][0]['geometry']['coordinates']


    if originalMapboxRouteDistanceMeters > routeDistanceMeters:
        optimisedData = scaleRoute(originalMapboxRouteCoordinates)
        recalculatePoints = optimisedData['recalculatePoints']
        response = requests.get(f'https://api.mapbox.com/directions/v5/mapbox/walking/{recalculatePoints}?alternatives=false&geometries=geojson&steps=true&continue_straight=false&access_token={MAPBOX_API_KEY}')
        data = response.json()
        optimisedMapboxCoordinates = data['routes'][0]['geometry']['coordinates']
        finiliseRouteData = finiliseRoute(optimisedMapboxCoordinates)
        viewBounds = routeBounds(finiliseRouteData['coordinates'])
        
        print(finiliseRouteData['distanceMeters'])
        print(finiliseRouteData['coordinates'])

        return jsonify({
            'distanceMeters': xx['distanceMeters'],
            'coordinates': xx['coordinates'],
            'mostNorthEastCoordinates': viewBounds['mostNorthEastCoordinates'],
            'mostSouthWestCoordinates': viewBounds['mostSouthWestCoordinates']
            })
    
    else:
        viewBounds = routeBounds(originalMapboxRouteCoordinates)
        return jsonify({
            'distanceMeters': originalMapboxRouteDistanceMeters,
            'coordinates': originalMapboxRouteCoordinates,
            'mostNorthEastCoordinates': viewBounds['mostNorthEastCoordinates'],
            'mostSouthWestCoordinates': viewBounds['mostSouthWestCoordinates']
            })
    


def scaleRoute(originalMapboxRouteCoordinates):
    mapboxRouteCoords = originalMapboxRouteCoordinates
    routeDistanceMeters = session['routeDistanceMeters']


    # Find distance of route:
    originCoords = mapboxRouteCoords[0]
    distanceMeters = 0
    for i in range(1, len(mapboxRouteCoords)):
        distanceMeters += haversineFormula(mapboxRouteCoords[i-1][1], mapboxRouteCoords[i][1], mapboxRouteCoords[i-1][0], mapboxRouteCoords[i][0])

    # Transfer route coords into dictionary:
    coordsDict = {}
    for i in range(len(mapboxRouteCoords)):
        coordsDict[i] = tuple(mapboxRouteCoords[i])

    # Generating list of distances:
    distanceLst = []
    for i in range(len(mapboxRouteCoords)):
        if i == 0 or i == len(mapboxRouteCoords) - 1:
            distanceLst.append(0)
        else:
            distanceFromOriginMeters = haversineFormula(originCoords[1], mapboxRouteCoords[i][1], originCoords[0], mapboxRouteCoords[i][0])
            distanceLst.append(distanceFromOriginMeters)

    # Optimising route that is greater than the route distance:
    if distanceMeters > routeDistanceMeters:
        # Pop furthest coordinate from origin off list:
        indexCoordMaxFromOrigin = distanceLst.index(max(distanceLst))
        coordsDict.pop(indexCoordMaxFromOrigin)

        #print(indexCoordMaxFromOrigin)

        optimisingIndex = indexCoordMaxFromOrigin + 1
        # Optimise route:
        while (distanceMeters > routeDistanceMeters) and (optimisingIndex in coordsDict):
            coordsDict.pop(optimisingIndex)
            optimisingIndex += 1
        
            # Recalculate distance:
            distanceMeters = 0
            for key in sorted(coordsDict.keys()):
                nextIndex = key + 1
                while (nextIndex not in coordsDict) and (nextIndex < max(coordsDict, key=int)):
                    nextIndex += 1
                if nextIndex in coordsDict:
                    distanceMeters += haversineFormula(coordsDict[key][1], coordsDict[nextIndex][1], coordsDict[key][0], coordsDict[nextIndex][0])

        if coordsDict[max(coordsDict, key=int)] != coordsDict[0]:
            secondLastToLast = True
            coordRecalculatePointOne = coordsDict[max(coordsDict, key=int)]
            coordRecalculatePointTwo = coordsDict[0]
            coordsDict[max(coordsDict, key=int) + 1] = coordsDict[0]
        else:
            secondLastToLast = False
            for key in sorted(coordsDict.keys()):
                currentIndex = key
                nextIndex = key + 1
                while (nextIndex not in coordsDict) and (nextIndex < max(coordsDict, key=int)):
                    nextIndex += 1
                if nextIndex - currentIndex > 1:
                    coordRecalculatePointOne = coordsDict[currentIndex]
                    coordRecalculatePointTwo = coordsDict[nextIndex]

    coordRecalculatePointOneLst = list(coordRecalculatePointOne)
    coordRecalculatePointTwoLst = list(coordRecalculatePointTwo)
    coordRecalculatePointOneString = str(coordRecalculatePointOneLst[0]) + ',' + str(coordRecalculatePointOneLst[1])
    coordRecalculatePointTwoString = str(coordRecalculatePointTwoLst[0]) + ',' + str(coordRecalculatePointTwoLst[1])
    
    recalculateRouteString = coordRecalculatePointOneString + ';' + coordRecalculatePointTwoString
    
    
    session['secondLastToLast'] = secondLastToLast
    session['coordsDict'] = coordsDict
    

    optimisedRouteLineString = { 
        'distanceMeters': distanceMeters,
        'coordinates': mapboxRouteCoords,
        'recalculatePoints':  recalculateRouteString
    }
        
    return optimisedRouteLineString

    
def finiliseRoute(optimisedMapboxCoordinates):
    
    missingRouteCoordinates = optimisedMapboxCoordinates
    
    secondLastToLast = session['secondLastToLast']
    coordsDict = session['coordsDict']
    coordsDict = {int(key):value for key, value in coordsDict.items()}

    listOriginalCoords = []
    for key in sorted(coordsDict.keys()):
        listOriginalCoords.append(list(coordsDict[key]))


    missingCoordsDict = {}
    for i in range(len(missingRouteCoordinates)):
        missingCoordsDict[i] = tuple(missingRouteCoordinates[i])

    for key in sorted(coordsDict.keys()):
        nextIndex = key + 1
        if nextIndex not in coordsDict:
            indexToCombine = key
            break
    
    if secondLastToLast:
        listOriginalCoords.pop()
        listOriginalCoords.pop()
        listCoords = []
        for i in listOriginalCoords:
            listCoords.append(i)
        for i in missingRouteCoordinates:
            listCoords.append(i)
        distanceMeters = 0
        for i in range(1, len(listCoords)):
            distanceMeters += haversineFormula(listCoords[i-1][1], listCoords[i][1], listCoords[i-1][0], listCoords[i][0])
    else:
        firstHalfListOriginalCoords = listOriginalCoords[:(indexToCombine)]
        secondHalfListOriginalCoords = listOriginalCoords[(indexToCombine+2):]
        listCoords = firstHalfListOriginalCoords + missingRouteCoordinates + secondHalfListOriginalCoords
        distanceMeters = 0
        for i in range(1, len(listCoords)):
            distanceMeters += haversineFormula(listCoords[i-1][1], listCoords[i][1], listCoords[i-1][0], listCoords[i][0])

    
    return { 'distanceMeters': distanceMeters, 'coordinates': listCoords }







app.run(port=5000)















    #X_coordsPolygon = [i[0] for i in coordsPolygon]
    #Y_coordsPolygon = [i[1] for i in coordsPolygon]
    #plt.plot(X_coordsPolygon, Y_coordsPolygon, linestyle='--', marker='o', color='b')
    #plt.plot(X_coordsPolygon[0], Y_coordsPolygon[0], linestyle='--', marker='o', color='r')
    #plt.grid()
    #plt.show()
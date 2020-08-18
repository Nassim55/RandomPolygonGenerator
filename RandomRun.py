import math
import random
import collections
import matplotlib.pyplot as plt
from haversineFormula import haversineFormula
from settings import *
from flask import Flask, jsonify, request, Response, session

@app.route('/route', methods=['GET'])
def getRandomRoute():
    original_longitude = float(request.args['longitude'])
    original_latitude = float(request.args['latitude'])
    routeDistanceMeters = float(request.args['routeDistance'])
    #print(original_longitude)
    #print(original_latitude)
    #print(routeDistanceMeters)

    # For use in haversine formula:
    earthRadiusMeters = 6371000
    
    # Polygon parameters:
    numberOfPoints = 5
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
    if perimeterIncrements > routeDistanceMeters:
        while perimeterIncrements > routeDistanceMeters:
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

    #print(perimeterIncrements)

    # Defining session variables:
    session['original_longitude'] = original_longitude
    session['original_latitude'] = original_latitude
    session['routeDistanceMeters'] = routeDistanceMeters
    session['perimeter'] = perimeterIncrements
    session['coordsPolygon'] = coordsPolygon
    session['randomRadiusLst'] = randomRadiusLst


    return jsonify({'coordinates': coordsPolygon})

@app.route('/optimise', methods=['POST'])
def scaleRoute():
    postRequest = request.get_json()
    mapboxRouteCoords = postRequest['mapboxRouteGeometry']
    routeDistanceMeters = session['routeDistanceMeters']
    
    # Find distance of route:
    originCoords = mapboxRouteCoords[0]
    distanceMeters = 0
    for i in range(len(mapboxRouteCoords)):
        distanceMeters += haversineFormula(mapboxRouteCoords[i-1][1], mapboxRouteCoords[i][1], mapboxRouteCoords[i-1][0], mapboxRouteCoords[i][0])
    print(distanceMeters)

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
        # Optimise route allowing for positive margin of error:
        while distanceMeters > (routeDistanceMeters + ((routeDistanceMeters/100)*5)):
            # Pop furthest coordinate from origin off list: 
            indexMaxDist = distanceLst.index(max(distanceLst))    
            distanceLst.pop(indexMaxDist)
            mapboxRouteCoords.pop(indexMaxDist)

            # Recalculate distance:
            distanceMeters = 0
            for i in range(len(mapboxRouteCoords)):
                distanceMeters += haversineFormula(mapboxRouteCoords[i-1][1], mapboxRouteCoords[i][1], mapboxRouteCoords[i-1][0], mapboxRouteCoords[i][0])
            print(distanceMeters)

    print(mapboxRouteCoords)
    
    optimisedRouteLineString = { 'distanceMeters': distanceMeters, 'coordinates': mapboxRouteCoords }
        
    return jsonify(optimisedRouteLineString)

    


            


    



    
    returnLst = []
    return jsonify({'optimisedCoordinates': returnLst})

    ##actualRouteDistanceMeters = 




app.run(port=5000)















    #X_coordsPolygon = [i[0] for i in coordsPolygon]
    #Y_coordsPolygon = [i[1] for i in coordsPolygon]
    #plt.plot(X_coordsPolygon, Y_coordsPolygon, linestyle='--', marker='o', color='b')
    #plt.plot(X_coordsPolygon[0], Y_coordsPolygon[0], linestyle='--', marker='o', color='r')
    #plt.grid()
    #plt.show()
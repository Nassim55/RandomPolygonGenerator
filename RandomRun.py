import math
import random
import collections
import matplotlib.pyplot as plt
from settings import *
from flask import Flask, jsonify, request, Response, session
import requests

from haversineFormula import haversineFormula
from routeBounds import routeBounds
from scaleRoute import scaleRoute
from finiliseRoute import finiliseRoute

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
        optimisedData = scaleRoute(originalMapboxRouteCoordinates, routeDistanceMeters)
        recalculatePoints = optimisedData['recalculatePoints']
        response = requests.get(f'https://api.mapbox.com/directions/v5/mapbox/walking/{recalculatePoints}?alternatives=false&geometries=geojson&steps=true&continue_straight=false&access_token={MAPBOX_API_KEY}')
        data = response.json()
        optimisedMapboxCoordinates = data['routes'][0]['geometry']['coordinates']
        finiliseRouteData = finiliseRoute(optimisedMapboxCoordinates, optimisedData['secondLastToLast'], optimisedData['coordsDict'])
        viewBounds = routeBounds(finiliseRouteData['coordinates'])
        
        print(finiliseRouteData['distanceMeters'])
        print(finiliseRouteData['coordinates'])

        return jsonify({
            'distanceMeters': finiliseRouteData['distanceMeters'],
            'coordinates': finiliseRouteData['coordinates'],
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
    







app.run(port=5000)
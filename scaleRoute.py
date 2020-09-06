from haversineFormula import haversineFormula

def scaleRoute(originalMapboxRouteCoordinates, routeDistanceMeters):
    mapboxRouteCoords = originalMapboxRouteCoordinates

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

    optimisedRouteLineString = { 
        'distanceMeters': distanceMeters,
        'coordinates': mapboxRouteCoords,
        'recalculatePoints':  recalculateRouteString,
        'secondLastToLast': secondLastToLast,
        'coordsDict': coordsDict
    }
        
    return optimisedRouteLineString
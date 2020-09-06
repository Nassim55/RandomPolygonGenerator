from haversineFormula import haversineFormula

def finiliseRoute(missingRouteCoordinates, secondLastToLast, coordsDict):
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
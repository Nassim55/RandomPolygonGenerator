def routeBounds(listCoords):
    listFinalisedLongitudes = []
    listFinalisedLatitudes = []
    for i in listCoords:
        listFinalisedLongitudes.append(i[0])
        listFinalisedLatitudes.append(i[1])
    
    return {
        'mostNorthEastCoordinates': [max(listFinalisedLongitudes), max(listFinalisedLatitudes)],
        'mostSouthWestCoordinates': [min(listFinalisedLongitudes), min(listFinalisedLatitudes)]
        }
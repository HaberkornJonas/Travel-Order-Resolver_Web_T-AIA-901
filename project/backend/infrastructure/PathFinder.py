# Imports
import numpy as np
from sknetwork.path import shortest_path
from model.Trip import Trip


class PathFinder:

    def __init__(self, trainStationNameToId, trainStationIdToName, tripGraph):
        self.trainStationNameToId = trainStationNameToId
        self.trainStationIdToName = trainStationIdToName
        self.tripGraph = tripGraph

    # Functions used to determine the shortest path between cities
    def getPathBetweenIds(self, trainStationStartIds: list, trainStationEndIds: list):
        paths = []
        # If start array contains one element also contained in end array -> return path from/to the same station
        for startId in trainStationStartIds:
            if startId in trainStationEndIds:
                return [int(startId), int(startId)]

        # As shortest_path() does not support multiple sources and multiple targets at the same time, we'll iterate through all start points and manually concat the results
        if (len(trainStationStartIds) > 1 and len(trainStationEndIds) > 1):
            for trainStationEndId in trainStationEndIds:
                results = shortest_path(self.tripGraph, sources=[int(i) for i in trainStationStartIds],
                                        targets=[int(trainStationEndId)], method='D')
                for result in results:
                    if len(result) >= 2:
                        paths.append(result)
            return paths
        else:
            results = shortest_path(self.tripGraph, sources=[int(i) for i in trainStationStartIds],
                                    targets=[int(i) for i in trainStationEndIds], method='D')
            for result in results:
                if len(result) >= 2:
                    paths.append(result)
            return paths

    def isCityMatchingKey(self, city: str, key: str):
        return city.lower() in key.lower()

    def getPathBetweenCities(self, start: str, end: str):
        trainStationStartIds = np.array([])
        trainStationEndIds = np.array([])

        # Get all stations that contains the searched name
        for key, value in self.trainStationNameToId.items():
            if self.isCityMatchingKey(start, key):
                trainStationStartIds = np.append(trainStationStartIds, value)
            if self.isCityMatchingKey(end, key):
                trainStationEndIds = np.append(trainStationEndIds, value)

        if len(trainStationStartIds) > 0 and len(trainStationEndIds) > 0:
            return self.getPathBetweenIds(trainStationStartIds, trainStationEndIds)
        else:
            return np.array([])

    def getBestPathForFullTrip(self, tripCityWaypoints: list):
        fullTrip = np.array(np.zeros(len(tripCityWaypoints) - 1), dtype=object)
        # Iterate through all sub trips
        for trip in range(len(fullTrip)):
            paths = self.getPathBetweenCities(tripCityWaypoints[trip], tripCityWaypoints[trip + 1])
            minDistance = None
            keptPath = None
            startId = None
            endId = None

            # Iterate though the returned array
            for path in paths:
                distance = 0
                # Nested array => multiple start/end possible
                if isinstance(path, list):
                    for i in range(len(path) - 1):
                        distance = distance + self.tripGraph[(path[i], path[i + 1])]
                    if minDistance is None or distance < minDistance:
                        minDistance = distance
                        keptPath = path
                        startId = path[0]
                        endId = path[len(path) - 1]

                # Scalar value => only one path possible
                else:
                    for i in range(len(paths) - 1):
                        distance = distance + self.tripGraph[(paths[i], paths[i + 1])]
                    minDistance = distance
                    keptPath = paths
                    startId = paths[0]
                    endId = paths[len(paths) - 1]

            fullTrip[trip] = Trip(startId, endId, keptPath, minDistance, self.trainStationIdToName)
        return fullTrip

    # TEST
    # Use following to test pathfinding functions above
    def testPathfinding(self):
        bestTrips = self.getBestPathForFullTrip(['Orléan', 'Paris', 'Strasbourg', 'dsfdsfd', 'Mulhouse', 'Mulhouse'])
        for i in range(len(bestTrips)):
            if bestTrips[i].path is not None:
                print(f"#{i + 1} - {bestTrips[i]}")
            else:
                if bestTrips[i].startStationId is None or bestTrips[i].endStationId is None:
                    print(f"#{i + 1} - Could not find one or both station of the sub-trip")
                else:
                    print(f"#{i + 1} - Could not find a path between the both stations")

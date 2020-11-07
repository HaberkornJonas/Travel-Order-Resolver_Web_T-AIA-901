class Trip:
    def __init__(self, startStationId, endStationId, path, totalDuration, trainStationIdToName):
        self.startStationId = startStationId
        self.endStationId = endStationId
        self.path = path
        self.trainStationIdToName = trainStationIdToName
        if totalDuration is None:
            self.totalDuration = None
        else:
            self.totalDuration = int(totalDuration)

    def __str__(self):
        return f"Trip from {self.trainStationIdToName[self.startStationId]} to {self.trainStationIdToName[self.endStationId]} for a total duration of {self.totalDuration} minutes by this path: {self.pathToString()}"

    def pathToString(self):
        string = ""
        for i in range(len(self.path)):
            if i > 0:
                string = string + " -> "
            string = string + self.trainStationIdToName[self.path[i]]
        return string
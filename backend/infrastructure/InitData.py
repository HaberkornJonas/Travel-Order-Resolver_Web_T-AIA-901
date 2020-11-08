# Imports
import os
import os.path
import csv
import numpy as np
from numpy.core._multiarray_umath import ndarray
from scipy.sparse import csr_matrix

from collections import defaultdict
import functools
import itertools


class InitData:

    pathCount = 0

    def __init__(self):
        # Create dictionary to associates a station name with an id
        self.trainStationNameToId = defaultdict(functools.partial(next, itertools.count()))
        self.trainStationIdToName = dict()
        self.trips = ndarray
        self.tripGraph = None
        self.init()

    def init(self):
        currentPath = os.getcwd()
        timeTableFileName = os.path.join(currentPath, 'data/timetables_edited.csv')
        with open(timeTableFileName, newline='', encoding='UTF-8') as csvFile:
            reader = csv.reader(csvFile, delimiter=',')

            csvFile.seek(0)
            next(reader)

            # First reading to get the number different stations and init shape of trips object
            for row in reader:
                idxA = self.trainStationNameToId[row[1]]
                idxB = self.trainStationNameToId[row[2]]
            numberOfTrainstations = len(self.trainStationNameToId)
            self.trips = np.zeros((numberOfTrainstations, numberOfTrainstations))

            # Reset of the reading position (ignoring header line)
            csvFile.seek(0)
            next(reader)

            # Reading data
            for row in reader:
                self.pathCount += 1
                idxA = self.trainStationNameToId[row[1]]
                idxB = self.trainStationNameToId[row[2]]

                # If trip already exist/has already be read, display message
                indexTupple = (idxA, idxB) if idxA < idxB else (idxB, idxA)
                if self.trips[indexTupple] != 0:
                    print(
                        f"Trip {row[1]} - {row[2]} with a distance of {row[3]} has already be read with a distance of {self.trips[indexTupple]}. Ignoring the new one.")
                else:
                    self.trips[indexTupple] = int(row[3])

            # Create dictionarry to map an id to its train station name
            self.trainStationIdToName = dict((id, name) for name, id in self.trainStationNameToId.items())

            # Make matrix symetrical as the trips are not directed but can be taken in both directions
            # Source from https://stackoverflow.com/a/42209263
            i_lower = np.tril_indices(numberOfTrainstations, -1)
            self.trips[i_lower] = self.trips.T[i_lower]

            # Creating Compressed Sparse Row (CSR) matrix to store and work more efficiently with only the trips
            self.tripGraph = csr_matrix(self.trips)

            print(f"Read {self.tripGraph.getnnz()} go and back trips ({int(self.tripGraph.getnnz() / 2)} distinc trips) out of {self.pathCount} rows for {len(self.trainStationNameToId)} distinct train stations.")
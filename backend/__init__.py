from flask import Flask, request

from infrastructure.InitData import InitData
from infrastructure.PathFinder import PathFinder
from infrastructure.LanguageProcessing import LanguageProcessing

import json

app = Flask(__name__)
app.config["DEBUG"] = True

# Init classes
initData = InitData()
pathFinder = PathFinder(initData.trainStationNameToId, initData.trainStationIdToName, initData.tripGraph)
languageProcessor = LanguageProcessing()

@app.route('/')
def home():
    return "<h2>🚋  Welcome, this is the Home page of our api's path finder.  🚋</h2> " \
           "<br>" \
           "You should try that endpoint 👉 /api/v1/getBestPath?phrase={yourSentenceHere}"

@app.route('/api/v1/getBestPath', methods=["GET"])
def userRequest():

    query_parameters = request.args

    userPhrase = query_parameters.get('phrase')

    capitalizedString = userPhrase.title()

    res = languageProcessor.analyseRequest(capitalizedString)

    print("res : ", res)

    return json.dumps(res)


if __name__ == "__main__":
    app.run()

from flask import Flask, request, jsonify
from flask_cors import CORS

from infrastructure.InitData import InitData
from infrastructure.PathFinder import PathFinder
from infrastructure.LanguageProcessing import LanguageProcessing

import json

app = Flask(__name__)
CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

# Init classes
initData = InitData()
pathFinder = PathFinder(initData.trainStationNameToId,
                        initData.trainStationIdToName, initData.tripGraph)
languageProcessor = LanguageProcessing()


@app.route('/')
def home():
    return "<h2>🚋  Welcome, this is the Home page of our path finder api's .  🚋</h2> " \
           "<br>" \
           "You should try that endpoint 👉 /api/v1/getBestPath?phrase={yourSentenceHere}"


@app.route('/api/v1/getBestPath', methods=["POST"])
def userPostRequest():

    userPhrase = request.get_data(as_text=True)

    res = languageProcessor.analyseRequest(userPhrase)

    return jsonify(res)


if __name__ == "__main__":
    app.run(host='0.0.0.0')

# @app.route('/api/v1/getBestPath', methods=["GET"])
# def userGetRequest():

#     query_parameters = request.args

#     if query_parameters.get('phrase'):

#         userPhrase = query_parameters.get('phrase')
#         print(userPhrase)

#         capitalizedString = userPhrase.title()

#         res = languageProcessor.analyseRequest(capitalizedString)

#         return jsonify(res)
#     else:
#         return "got no request"

from flask import Flask, render_template, request, redirect, make_response, Response, send_from_directory, send_file
import time
import datastore
import json

app = Flask(__name__)


@app.route("/")
def main():
    topCost = datastore.topCost(10)
    print(topCost)
    resp = make_response(render_template("index.html", topCost=topCost))
    return resp


@app.route("/getTraceData", methods=['GET'])
def getTraceData():

    traceId = int(request.args.get("traceid"))
    traceData = datastore.getTraceData(traceId)
    traceData = json.dumps(datastore.transform(traceData))
    return Response(traceData, status=200, mimetype='application/json')

@app.route("/phaseavg", methods=['GET'])
def getphaseavg():
    phaseavgdata = json.dumps(datastore.getPhaseAvg())
    print(phaseavgdata)
    return Response(phaseavgdata, status=200, mimetype='application/json')

if __name__ == "__main__":
    app.run(host='0.0.0.0', use_reloader=False)
# TODO: MAANYA FIGURE OUT HOW TO EDIT TIME RESPONSE TO RETURN JUST MINUTES

from datetime import datetime, timezone
from flask import Flask, jsonify,request
from flask_cors import CORS
import requests

app = Flask(__name__)  # Creates a Flask Client
CORS(app)

# Dict from Transloc Route IDs to Route Name
route_codes = { "4012616": "A", "4012618": "B", "4012620": "C", "4012628": "H", "4012632": "REXB"}

@app.route("/")
def get_bus_times():
    stop_1 = requests.get("https://transloc-api-1-2.p.rapidapi.com/arrival-estimates.json",headers={"x-rapidapi-key": "5466eef685msh86a898d149e8ee7p1a3b80jsn3f9a412c0ead"}, params={"stops":"4231636","agencies":"1323"}).json()
    stop_2 = requests.get("https://transloc-api-1-2.p.rapidapi.com/arrival-estimates.json",headers={"x-rapidapi-key": "5466eef685msh86a898d149e8ee7p1a3b80jsn3f9a412c0ead"}, params={"stops":"4229508","agencies":"1323"}).json()
    
    stop_1_times = format_arrival(stop_1)
    stop_2_times = format_arrival(stop_2)

    all_times = stop_1_times + stop_2_times

    return jsonify({"all_times" : all_times})
    

def format_arrival(stop):
    
    all_times = ""
    
    for prediction in stop['data'][0]['arrivals']:
        arrival_time = int((datetime.fromisoformat(prediction['arrival_at']).replace(tzinfo = None)-datetime.now()).seconds / 60)
        bus_name = route_codes[prediction['route_id']]
        time = "{} : {} minutes".format(bus_name, arrival_time)
        all_times += time + "\n"
    
    return all_times


if __name__ == "__main__":
    app.run()

from flask import Flask, request
from haversine import haversine
import json
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app, supports_credentials=True)


@app.route('/distance/cep1/<cep1>/cep2/<cep2>', methods=['GET'])
def get_kilometers_distance(cep1, cep2):
    response = { "result" : get_distance(cep1, cep2)}
    return json.dumps(response)


def get_address(cep):
    address = requests.get(f'https://cep.awesomeapi.com.br/json/{cep}')
    return json.loads(address.text)


def get_distance(cep1, cep2):
    addressA = get_address(cep1)
    addressB = get_address(cep2)

    pointOne = (float(addressA['lat']), float(addressA['lng']))  # (lat, lon)
    pointTwo = (float(addressB['lat']), float(addressB['lng']))

    distance = haversine(pointOne, pointTwo, unit='km')
    result = {
        "addressA": addressA,
        "addressB": addressB,
        "distance_points_km": distance
    }

    return result


if __name__ == "__main__":
    app.run(debug=True)

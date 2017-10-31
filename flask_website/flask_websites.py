"""
Web app that controlls other web applications
"""

import flask
import config
from flask import request
import logging
import geocoder
import requests

# Globals
app = flask.Flask(__name__)
CONFIG = config.configuration()
app.secret_key = CONFIG.SECRET_KEY
app.debug = CONFIG.DEBUG

if app.debug:
    app.logger.setLevel(logging.DEBUG)


# Pages
@app.route("/")
@app.route("/index")
def index():
    app.logger.debug("Enter home page")
    return flask.render_template('index.html')


@app.route("/findmyicecream")
def findmyicecream():
    app.logger.debug("Enter find my ice cream page")
    flask.g.topic = CONFIG.FIND
    flask.session['topic'] = CONFIG.FIND
    return flask.render_template('findmyicecream.html')


# Error handlers
@app.errorhandler(404)
def error_404(e):
    app.logger.warning("++ 404 error: {}".format(e))
    return flask.render_template('404.html'), 404


@app.errorhandler(500)
def error_500(e):
    app.logger.warning("++ 500 error: {}".format(e))
    assert not True  # I want to invoke the debugger
    return flask.render_template('500.html'), 500


@app.errorhandler(403)
def error_403(e):
    app.logger.warning("++ 403 error: {}".format(e))
    return flask.render_template('403.html'), 403


# Map setup
@app.route("/_setup_map")
def setup_map():
    """
    Sends map location and key information to set up map.
    """
    information = {"lat": float(CONFIG.DEFAULT_LAT),
                   "lng": float(CONFIG.DEFAULT_LNG),
                   "mapbox": CONFIG.MAPBOX}
    return flask.jsonify(result=information)


# Geocoding
@app.route("/_get_addy")
def get_addy():
    """
    With an input of latitude and longitude, sends a
    JSON file with the information of the address.
    """
    app.logger.debug("Got JSON request")
    lat = request.args.get('lat', type=float)
    lng = request.args.get('lng', type=float)

    app.logger.debug('latitude: {}'.format(lat))
    app.logger.debug('longitude: {}'.format(lng))

    g = geocoder.google([lat, lng], method='reverse')
    app.logger.debug("g.json: {}".format(g.json))
    return flask.jsonify(result=g.json)


@app.route("/_get_poi")
def get_poi():
    """
    Gets the address of the points of interest specified
    in the credentials file in a 10,000 meter radius.
    """
    lat = request.args.get('lat', type=float)
    lng = request.args.get('lng', type=float)
    url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
    location = "{},{}".format(lat, lng)
    params = {"key": CONFIG.GOOGLE_KEY,
              "location": location,
              "radius": CONFIG.RADIUS,
              "keyword": CONFIG.FIND}
    # Requests encodes the comma with percent so a work around for that problem
    params_str = "&".join("{}={}".format(k, v) for k, v in params.items())
    r = requests.get(url, params=params_str)
    return flask.jsonify(r.json()['results'])


if __name__ == "__main__":
    print("Opening for global access on port {}".format(CONFIG.PORT))
    app.run(host="0.0.0.0")

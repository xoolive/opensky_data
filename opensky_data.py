import configparser
import time
from datetime import datetime, timedelta
from pathlib import Path

import maya
import requests
from opensky_data.impala import ImpalaWrapper


def name_request(query):

    params = {'format': 'json', 'limit': 1, 'dedupe': 0,
              'polygon_geojson': 1, 'q': query}
    url = 'https://nominatim.openstreetmap.org/search'
    response = requests.post(url, timeout=30, params=params)
    try:
        json = response.json()
    except Exception:
        # 429 is 'too many requests' and 504 is 'gateway timeout' from server
        # overload - handle these errors by recursively calling until we get
        # a valid response
        if response.status_code in [429, 504]:
            # pause for error_pause_duration seconds before re-trying request
            time.sleep(1)
            return name_request(query)

        # else, this was an unhandled status_code, throw an exception
        else:
            raise Exception('Server returned no JSON data.\n{} {}\n{}'.format(
                response, response.reason, response.text))

    return json[0]['boundingbox']


def opensky_data(date, until, output_file, settings, bounds, **kwargs):

    if bounds is not None:
        south, north, west, east = name_request(bounds)
        bounds = west, south, east, north

    before = datetime.fromtimestamp(maya.parse(date).epoch)
    if until is None:
        until = before + timedelta(days=1)

    config = configparser.ConfigParser()
    config.read(settings.as_posix())
    username = config.get("global", "opensky_username", fallback="")
    password = config.get("global", "opensky_password", fallback="")
    opensky = ImpalaWrapper(username, password)

    data = opensky.history(before, until, bounds=bounds, **kwargs)

    if output_file.suffix == '.pkl':
        data.to_pickle(output_file.as_posix())

    if output_file.suffix == '.csv':
        data.to_csv(output_file.as_posix())

    if output_file.suffix == '.h5':
        data.to_hdf(output_file.as_posix())

    if output_file.suffix == '.xlsx':
        data.to_excel(output_file.as_posix())


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(
        description="Get data from OpenSky records")

    parser.add_argument("date", help="start date for trajectories")

    parser.add_argument(
        "-u", dest="until", default=None,
        help="end date for trajectories (default: date + 1 day)")

    parser.add_argument(
        "-o", dest="output_file", default='output.csv', type=Path,
        help="output file for trajectories (default: output.csv)")

    parser.add_argument(
        "-c", dest="callsign",
        help="callsign for one flight")

    parser.add_argument(
        "-b", dest="bounds",
        help="bounding box for trajectories (location name)")

    parser.add_argument(
        "-s", dest="settings", type=Path, default="settings.cfg",
        help="setting file with login information")

    args = parser.parse_args()

    opensky_data(**vars(args))

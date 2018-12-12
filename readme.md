## Python interface to the OpenSky Network Impala shell

Xavier Olive, 2018  
MIT license

**No longer maintained: this repository is no longer active.  
There *are* bugs that will not be fixed here.  
The same functionality is available in the actively developped
[traffic](https://github.com/xoolive/traffic) Python library.**


## Requirements

```sh
git clone git+https://github.com/xoolive/opensky_data
cd opensky_data
pip install -r requirements
```

## Usage

A basic script is given as an example call to the API.

**Edit the `settings.cfg` file with your credentials for the Impala shell.**

```
usage: opensky_data.py [-h] [-u UNTIL] [-o OUTPUT_FILE] [-c CALLSIGN]
                       [-b BOUNDS] [-s SETTINGS]
                       date

Get data from OpenSky records

positional arguments:
  date            start date for trajectories

optional arguments:
  -h, --help      show this help message and exit
  -u UNTIL        end date for trajectories (default: date + 1 day)
  -o OUTPUT_FILE  output file for trajectories (default: output.csv)
  -c CALLSIGN     callsign for one flight
  -b BOUNDS       bounding box for trajectories (location name)
  -s SETTINGS     setting file with login information
```

Get flight `DLH66N` on November 23rd 2017 (OpenSky Workshop day!):
```sh
python opensky_data.py 2017-11-23 -c DLH66N -o DLH66N.csv
```

Get all trajectories over (the bounding box of) Switzerland between 6am and
7am (UTC) on January 1st:
```sh
python opensky_data.py 2018-01-01T06:00 -u 2018-01-01T07:00 -b Switzerland
```

See an example of the API usage in `notebook.ipynb`.

## Under the hood

Each request is split hour by hour (see indexing issues on [Impala
page](https://opensky-network.org/impala-guide)) and put
in cache in the default temporary directory of your OS. After each iteration, a
`pandas` dataframe is created from a modified version of the cached data (robust
to network issues...): all dataframes are then concatenated and exported based
on the extension of the output file.

## Contribution

For now, only the trajectory history use case has been addressed. Feel free to
contributed with a pull request if you see any contribution that can be useful
to the community.

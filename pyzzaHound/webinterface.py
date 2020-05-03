import json
import os
import numpy as np
import datetime
import bottle

import SensorDB
import common  # for logging

logger = common.get_logger(__name__)

# create database interface
di = SensorDB.DataInterface()

@bottle.route('/<path:path>')
def serve_static_files(path):
    cwd = os.getcwd()
    parent = os.path.dirname(cwd)
    app_dir = os.path.join(parent, 'webHound')
    return bottle.static_file(path, app_dir)


@bottle.get('/testing/<test>')
def testing(test):
    t = test
    return json.dumps(t)


@bottle.get('/sensor-api/getTemp')
def get_temp():

    tstart = bottle.request.query.tstart
    tstop  = bottle.request.query.tstop
    device = bottle.request.query.device.lower()

    tstart = ' '.join(tstart.split('T'))[:-6]  # -6 to slice off timezone
    tstop = ' '.join(tstop.split('T'))[:-6]

    # format tstart, tstop
    tstart = datetime.datetime.strptime(tstart, '%Y-%m-%d %H:%M:%S')
    tstop  = datetime.datetime.strptime(tstop, '%Y-%m-%d %H:%M:%S')

    # get the data from the database
    device, time, tempc, tempf, stats = di.get_temp_readings(tstart, tstop, device)

    return_dict = {
        'name': device,
        'time': time,
        'tempc': tempc,
        'tempf': tempf,
        'stats': stats
    }
    json_str = json.dumps(return_dict)
    return json_str


@bottle.route('/doyle-api/basic-plot')
def basic_plot():
    """
    return a json string for testing a basic plot
    :return:
    """
    x = np.arange(0, 10, .1)
    y = np.random.random(100)

    return_dict = dict()
    return_dict['x'] = list(x)
    return_dict['y'] = list(y)

    json_str = json.dumps(return_dict)
    return json_str


@bottle.get('/doyle-api/basic-get')
def basic_get():
    name    = bottle.request.query.name
    purpose = bottle.request.query.purpose
    urine   = bottle.request.query.urine

    output = '%s is a good boyle who loves to %s and pees %s' % (name, purpose, urine)

    json_str = json.dumps(output)

    return json_str


@bottle.route('/doyle-api/hello')
def hello():
    doyle_says = 'hello'
    return json.dumps(doyle_says)

bottle.run(host='localhost', port=8080, debug=True)


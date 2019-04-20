import numpy as np
from bottle import Bottle, run, request
import json


app = Bottle()


@app.route('/doyle-api/basic-plot')
def basic_plot():
    x = np.arange(0, 10, .1)
    y = np.random.random(100)

    return_dict = dict()
    return_dict['x'] = list(x)
    return_dict['y'] = list(y)

    json_str = json.dumps(return_dict)
    return json_str


@app.get('/doyle-api/basic-get')
def basic_get():
    name    = request.query.name
    purpose = request.query.purpose
    urine   = request.query.urine

    output = '%s is a good boyle who loves to %s and pees %s' % (name, purpose, urine)

    json_str = json.dumps(output)

    return json_str


@app.route('/doyle-api/hello')
def hello():
    doyle_says = 'hello'
    return json.dumps(doyle_says)


run(app, host='localhost', port=8080)



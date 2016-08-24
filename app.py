#! /usr/bin/python
'''
    App Service for DC Jeeves

    This application is meant to:
        1. accept REST calls associated with the utterance file.
        2. Validate the request.
        3. Translate what is meant to be done into the associated backend datacenter call.
        4. Pass on a response back to the client.

'''
__author__ = 'mytokarz'

from flask import Flask, Response
from dcjeevestree import dcjeevestree
import re

app_dir = "./"
utterance_file = app_dir + "utterance.conf"


tree = dcjeevestree()
with open(utterance_file) as f:
    for line in f:
        if not re.match('^\s*#', line): # ignore comments
            if not re.match('^\s*$', line): # ignore empty lines
                line = line.rstrip()
                tree.add(line)

print tree.getjson()







exit()

app = Flask(__name__)

@app.route('/help')



def print_help():
    '''
    Build a help response.
    '''


    resp = Response(
        content_type='application/json',
        headers={"Usage": utterance_lines},
        status=200)
    return resp


@app.route('/')
def hello_world():
    return 'Hello, MIKE1'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

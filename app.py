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

from flask import Flask, Response, send_from_directory, redirect,request
from dcjeevestree import dcjeevestree
import os
import re

# define static variables
app_dir = "./"
utterance_file = app_dir + "utterance.conf"
tree = dcjeevestree()

# Read in the utterance config file
def readinconfigs():
    global tree
    with open(utterance_file) as f:
        for line in f:
            if not re.match('^\s*#', line): # ignore comments
                if not re.match('^\s*$', line): # ignore empty lines
                    line = line.rstrip()
                    tree.add(line)


readinconfigs()

app = Flask(__name__)

@app.route('/json')
def print_json():
    '''
    Return JSON version of utterance file.
    '''
    return  tree.getjson(), 200, {'content_type': 'application/json'}

@app.route('/validate')
def validate_sentence():
    '''
    Validate an utterance is supported.
    '''
    if request.args.get("sentence") and tree.includes(request.args.get("sentence")):
        return "looks good!", 200, {'content_type': 'text/html'}
    else:
        return "I don't understand this, try <A href='/help'>/help", 200, {'content_type': 'text/html'}

@app.route('/go')
def dcjeeves_go():
    '''
    Return JSON version of utterance file.
    '''
    return  tree.getjson(), 200, {'content_type': 'application/json'}


@app.route('/help')
def print_help():
    '''
    Build a help response.
    '''
    return send_from_directory(os.path.join(app_dir,'static'),'app-help.html'), 200, {'content_type': 'text/html'}


@app.route('/')
def hello_world():
    return redirect("/help", code=302)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

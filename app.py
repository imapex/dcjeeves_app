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
from dcjeevessentence import dcjeevessentence
from scrawl import scrawl
import os
import re
import json

# define static variables
app_dir = "./"
utterance_file = app_dir + "utterance.conf"
scrawl_file = app_dir + "scrawl.yaml"
tree = dcjeevestree()
response_json = {}
get_help = "Try navigating to /help."

# Read in the utterance config file
def readinconfigs():
    # Read in the utterance file
    global tree
    with open(utterance_file) as f:
        for line in f:
            if not re.match('^\s*#', line): # ignore comments
                if not re.match('^\s*$', line): # ignore empty lines
                    line = line.rstrip()
                    tree.add(line)
    # Read in the scrawl file
    scrawls = scrawl(scrawl_file)

def validate_request(sentence):
    response_json["Sentence"]=sentence
    print "Validating sentence: "+sentence
    dcjsentence = dcjeevessentence(sentence)
    if not dcjsentence.parse():
        print "Sentence passed in failed ot parse"
        response_json["Details"] = "Sentence not found in utterance file. "+get_help
    else:
        if tree.includes(sentence):
            print "Sentence found in utterance file"

            if scrawlfile.validateenvcloud(dcjsentence.environment,dcjeevessentence.cloud):
                print "ENVIRONMENT and CLOUD found in scrawl file"
                response_json["Details"] = sentence
                response_json["Valid"] = "true"
            else:
                response_json["Details"] = "(ENVIRONMENT|CLOUD) combination ("+ dcjsentence.environment+"|"+dcjeevessentence.cloud+") not found in scrawl file. "+get_help
        else:
            print "Sentence not found in utterance file"
            response_json["Details"] = "Sentence not found in utterance file. "+get_help
    response_json["Valid"] = "false"
    return 0

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
    if ('sentence' in request.args):
        valid = validate_request(request.args.get("sentence"))
        if valid:
            return json.dumps(response_json,indent=4), 200, {'content_type': 'application/json'}
    else:
        return json.dumps({ "Valid": "false", "Details": "Sentence not passed in" },indent=4), 400, {'content_type': 'application/json'}
    return json.dumps(response_json,indent=4), 400, {'content_type': 'application/json'}

@app.route('/go')
def dcjeeves_go():
    '''
    Return
    '''
    if ('sentence' in request.args):
        valid = validate_request(request.args.get("sentence"))
        if valid:
            # Replace with back end execution
            return json.dumps(response_json,indent=4), 200, {'content_type': 'application/json'}
    else:
        return json.dumps({ "Valid": "false", "Details": "Sentence not passed in" },indent=4), 400, {'content_type': 'application/json'}
    return json.dumps(response_json,indent=4), 400, {'content_type': 'application/json'}

@app.route('/scraw')
def dcjeeves_scrawlhelp():
    return "Hi", 200, {'content_type': 'application/json'}

@app.route('/help')
def print_help():
    '''
    Build a help response.
    '''
    return send_from_directory(os.path.join(app_dir,'static'),'app-help.html'), 200, {'content_type': 'text/html'}


@app.route('/')
def main_landing():
    return redirect("/help", code=302)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)


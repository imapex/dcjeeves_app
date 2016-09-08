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

from flask import Flask, send_from_directory, redirect,request
from dcjeevestree import dcjeevestree
from dcjeevessentence import dcjeevessentence
from scrawl import scrawl
from dcjbroker import dcjbroker
import os
import re
import json

# define static variables
# ----------------------------------------------#-------------------------------------------#
app_dir = "./"                                  # - application directory                   #
utterance_file = app_dir + "utterance.conf"     # - location of utterance file              #
scrawl_file = app_dir + "scrawl.yaml"           # - location of scrawl file                 #
tree = dcjeevestree()                           # - build a data structure from utt file    #
response_json = {}                              # - holds the json response                 #
get_help = "Try navigating to /help."           # - string to append to all bad requests    #
scrawls = scrawl(scrawl_file)                   # - build a data structure from scrawl file #
# ----------------------------------------------#-------------------------------------------#


def readinconfigs():
    '''
    # Read in the utterance file
    # To Do: This should be moved to a class long term like the scrawl file
    '''
    global tree
    with open(utterance_file) as f:
        for line in f:
            if not re.match('^\s*#', line): # ignore comments
                if not re.match('^\s*$', line): # ignore empty lines
                    line = line.rstrip()
                    tree.add(line)


def validate_request(sentence):
    '''
    # Validate the sentenece passed in.  Syntax as well as scrawl mappings will be checked.

    :rtype : object
    '''
    response_json["Sentence"]=sentence
    print ("Validating sentence: "+sentence)
    dcjsentence = dcjeevessentence(sentence)

    if not dcjsentence.parsed:
        print ("Sentence passed in failed ot parse")
        response_json["Details"] = "Sentence not found in utterance file. "+get_help
    else:
        if tree.includes(sentence):
            print ("Sentence found in utterance file")
            if scrawls.validateenvcloud(dcjsentence.environment, dcjsentence.cloud):
                print ("ENVIRONMENT ("+dcjsentence.environment+") and CLOUD ("+dcjsentence.cloud+") found in scrawl file")
                response_json["Details"] = "OK"
                response_json["Valid"] = "true"
                return 1
            else:
                response_json["Details"] = "(ENVIRONMENT|CLOUD) combination (" + dcjsentence.environment + "|" + dcjsentence.cloud+") not found in scrawl file. "+get_help
        else:
            print ("Sentence not found in utterance file")
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
            broker = dcjbroker(request.args.get("sentence"),scrawls)
            response_json["Details"] = broker.execute()
            return json.dumps(response_json,indent=4), 200, {'content_type': 'application/json'}
    else:
        return json.dumps({ "Valid": "false", "Details": "Sentence not passed in" },indent=4), 400, {'content_type': 'application/json'}
    return json.dumps(response_json,indent=4), 400, {'content_type': 'application/json'}


@app.route('/scrawl')
def dcjeeves_scrawlhelp():
    print(scrawls.listenvcloud())
    return json.dumps(scrawls.listenvcloud(),indent=4), 200, {'content_type': 'application/json'}


@app.route('/help')
def print_help():
    '''
    Build a help response.
    '''
    return send_from_directory(os.path.join(app_dir,'static'),'app-help.html'), 200, {'content_type': 'text/html'}


@app.route('/')
def main_landing():
    '''
    #If landing page hit, redirect to human readable help
    #:return: redirect
    '''
    return redirect("/help", code=302)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)


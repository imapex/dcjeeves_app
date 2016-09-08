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

import urllib3
import requests

urllib3.disable_warnings()


class ucsdworker():



    def __init__(self,ip,restapikey):
        self.ip = ip
        self.restapikey = restapikey

    def go(self):
        print("hi")

    def execute(self,command,params):

        # auto-generate the name of the workflow based on the command
        wfname = "DCJeeves"
        for k in command.split():
            wfname+="-"+k.upper()

        # Build the JSON needed to call UCSD workflows
        json={}
        json['param0']=wfname

        params1list = []
        for k in params.keys():
            dict1 = {}
            dict1['name']=k
            dict1['value']=params[k]
            params1list.append(dict1)
        print(params1list)
        dict1 = {}
        dict1['list']=params1list
        json['param1']=dict1
        json['param2']='-1'


        # Create the headers needed for UCSD
        headers = {}
        headers['X-Cloupia-Request-Key']=self.restapikey


        # Build the URL to call
        url = 'https://'+self.ip+'/app/api/rest?formatType=json&opName=userAPISubmitWorkflowServiceRequest&opData='+str(json)


        print("UCSD passed JSON: "+str(json))
        print("UCSD passed headers: "+str(headers))
        print("UCSD GET URL: "+url)


        r = requests.get(url, headers=headers, verify=False)

        print ("UCSD Response: "+r.text)


        return r.text


# Used for standalone testing
#jsoninput = '{ param0:"DCJeeves-REBOOT-VM",param1:{"list":[{"name":"vm name","value":"snoopy"},{"name":"environment","value":"DCJeeves-DEV"}]},param2:-1}'
#print ("My JSON data is: "+jsondata)


#url = 'https://10.91.86.212/app/api/rest?formatType=json&opName=userAPISubmitWorkflowServiceRequest&opData='+jsondata
#headers = {'X-Cloupia-Request-Key': 'D69924992E90481D9415D8C5843E1934'}
#r = requests.get(url, headers=headers, verify=False)


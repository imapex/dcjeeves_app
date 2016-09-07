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

import requests

import urllib3
urllib3.disable_warnings()




# Used for standalone testing
jsondata = '{ param0:"DCJeeves-REBOOT-VM",param1:{"list":[{"name":"vm name","value":"snoopy"},{"name":"environment","value":"DCJeeves-DEV"}]},param2:-1}'
print ("My JSON data is: "+jsondata)


url = 'https://10.91.86.212/app/api/rest?formatType=json&opName=userAPISubmitWorkflowServiceRequest&opData='+jsondata
headers = {'X-Cloupia-Request-Key': 'D69924992E90481D9415D8C5843E1934'}

#ctx = ssl.SSLContext(ssl.)
# set other SSLContext options you might need
#response = urllib2.urlopen(url, context=ctx, headers=headers)
r = requests.get(url, headers=headers, verify=False)

print (r.text)

# s=requests.Session()
# s.mount('https://10.91.86.212', SslAdapter())
# s.get(url,verify=False,headers=headers)

#
# {
#
#     param0:"DCJeeves-REBOOT-VM",
#
#     param1:{
#
#                 "list":[
#
#                     {"name":"vm name","value":"snoopy"},
#
#                     {"name":"environment","value":"DCJeeves-DEV"}
#
#                 ]
#
#             },
#
#     param2:-1
#
# }
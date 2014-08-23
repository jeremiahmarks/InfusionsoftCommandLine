#!/usr/bin/python

#This will serve to start the IS command line software, taking care of basic imports etc. 

import xmlrpclib

appname=""
apikey=""

class Server:
    def __init__(self, url, key):
        self.url=url
        self.apiKey=key
        self.connection = xmlrpclib.ServerProxy(self.url)


def createServer():
    if (appname==""):
        appname=raw_input("Please enter appname: ")
    if (apikey==""):
        apikey=raw_input("Please enter API key: ")

    serverURL = "https://" + appname + ".infusionsoft.com:443/api/xmlrpc")

    thisServer=Server(serverURL, apikey)

    return thisServer




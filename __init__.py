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

    def getAllContacts(self):
        """
        This method will do an initial search for all contacts that have an email address.
        It will display all results. 
        If there are 15 results it will increment the page number and do the search again. 
        If there are less than 15 results it will set the page number to zero then search for all contacts without an email address
        It will display all results.
        If there are 15 results it will increment the page number and do the search again. 
        If there are less than 15 results it will quit.

        It appears that searching for "%" will return fields with blank values as well, so I am commenting out
        the lines of code that also search for blank emails.
        """
        page=0
        contactNo=0
        query = {'Email': '%'}
        resultsPerPage=15
        desiredInfo=["FirstName", "LastName", "Email"]
        while True:
            results=self.tableQuery(query, resultsPerPage,page)
            page+=1
            if(len(results)>0):
                for contactRecord in results:
                    printString= str(contactNo) + ". Name: "
                    if (contactRecord.has_key("FirstName")):
                        printString=printString + contactRecord["FirstName"] + " "
                    if (contactRecord.has_key("LastName")):
                        printString=printString + contactRecord["LastName"] + " "
                    printString = printString + "Email: "
                    if (contactRecord.has_key("Email")):
                        printString=printString + contactRecord["Email"]
                    printString = printString + "\n"
                    print printString
                    contactNo+=1
            if (len(results)<resultsPerPage):
                break
        page=0
        query = {'Email': ''}
#        while True:
#            results=self.tableQuery(query, resultsPerPage,page)
#            for contactRecord in results:
#                printString= str(contactNo) + ". Name: "
#                if (contactRecord.has_key("FirstName")):
#                    printString=printString + contactRecord["FirstName"] + " "
#                if (contactRecord.has_key("LastName")):
#                    printString=printString + contactRecord["LastName"] + " "
#                printString = printString + "Email: "
#                if (contactRecord.has_key("Email")):
#                    printString=printString + contactRecord["Email"]
#                printString = printString + "\n"
#                print printString
#                contactNo+=1
#            if (len(results)<resultsPerPage):
#                break        

    def tableQuery(self, query, resultsPerPage, pageNumber, sortedBy="Email", ascending=True, table="Contact", desiredInfo=["FirstName", "LastName", "Email"]):
        return self.connection.DataService.query(self.apiKey, table, resultsPerPage, pageNumber, query, desiredInfo,sortedBy,ascending)


def createServer():
    global appname
    global apikey
    if (appname==""):
        appname=raw_input("Please enter appname: ")
    if (apikey==""):
        apikey=raw_input("Please enter API key: ")

    serverURL = "https://" + appname + ".infusionsoft.com:443/api/xmlrpc"

    thisServer=Server(serverURL, apikey)

    return thisServer

if (__name__=="__main__"):
    server=createServer()
    server.getAllContacts()


#!/usr/bin/python

#This will serve to start the IS command line software, taking care of basic imports etc.

import xmlrpclib

appname=""
apikey=""

allContactFields=["AccountId", "Address1Type", "Address2Street1", "Address2Street2", "Address2Type", "Address3Street1", "Address3Street2", "Address3Type", "Anniversary", "AssistantName", "AssistantPhone", "BillingInformation", "Birthday", "City", "City2", "City3", "Company", "CompanyID", "ContactNotes", "ContactType", "Country", "Country2", "Country3", "CreatedBy", "DateCreated", "Email", "EmailAddress2", "EmailAddress3", "Fax1", "Fax1Type", "Fax2", "Fax2Type", "FirstName", "Groups", "Id", "JobTitle", "LastName", "LastUpdated", "LastUpdatedBy", "LeadSourceId", "Leadsource", "MiddleName", "Nickname", "OwnerID", "Password", "Phone1", "Phone1Ext", "Phone1Type", "Phone2", "Phone2Ext", "Phone2Type", "Phone3", "Phone3Ext", "Phone3Type", "Phone4", "Phone4Ext", "Phone4Type", "Phone5", "Phone5Ext", "Phone5Type", "PostalCode", "PostalCode2", "PostalCode3", "ReferralCode", "SpouseName", "State", "State2", "State3", "StreetAddress1", "StreetAddress2", "Suffix", "Title", "Username", "Validated", "Website", "ZipFour1", "ZipFour2", "ZipFour3"]

class Server:
    global allContactFields
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
        desiredInfo=allContactFields
        while True:
            results=self.tableQuery(query, resultsPerPage,page, desiredInfo=desiredInfo)
            page+=1
            if(len(results)>0):
                for contactRecord in results:
                    printString=""
                    for eachField in desiredInfo:
                        if (contactRecord.has_key(eachField)):
                            printString=printString+" "+eachField+": "+ str(contactRecord[eachField])
                        else:
                            printString=printString+" "+eachField+": NA"
                    print printString + "\n"

#                    printString= str(contactNo) + ". Name: "
#                    if (contactRecord.has_key("FirstName")):
#                        printString=printString + contactRecord["FirstName"] + " "
#                    if (contactRecord.has_key("LastName")):
#                        printString=printString + contactRecord["LastName"] + " "
#                    printString = printString + "Email: "
#                    if (contactRecord.has_key("Email")):
#                        printString=printString + contactRecord["Email"]
#                    printString = printString + "\n"
#                    print printString
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

    def allContactsAllFields(self):
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
        desiredInfo=allContactFields
        results=self.tableQuery(query, resultsPerPage,page)
        return results

    def tableQuery(self, query, resultsPerPage, pageNumber, sortedBy="Email", ascending=True, table="Contact", desiredInfo=["FirstName", "LastName", "Email"]):
        return self.connection.DataService.query(self.apiKey, table, resultsPerPage, pageNumber, query, desiredInfo,sortedBy,ascending)

    def clearScreen(self):
        print chr(27) + "[2J"

    def getFile(self):
        self.clearScreen()
        print ""
        importingFile=open(raw_input("Please enter location of the file: \n"),"r")


    def menuPrint(self):
        print chr(27) + "[2J"
        print "*************************************************"
        print "**  Infusionsoft Command Line                  **"
        print "**                                             **"
        print "**   (D)isplay all contacts                    **"
        print "**   (Q)uit                                    **"
        print "**                                             **"
        print "*************************************************"
        self.currentAction=raw_input("Please make a selection: ")
        if (self.currentAction=="D") or (self.currentAction=="d"):
            self.getAllContacts()
            raw_input("Press Enter to continue")
        if (self.currentAction=="Q") or (self.currentAction=="q"):
            return 0
        self.menuPrint()


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
    server.menuPrint()


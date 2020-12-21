import os
from mailchimp3 import MailChimp
from consts import *
from certsDictionary import *
from subscriberHash import subHashGen

client = MailChimp(mc_api = apiKey, mc_user = username, timeout=50.0)


# ---------- Upload Certificates from local to Mailchimp Content Studio ----------

# generate cert dictionary with keys=filename and values=encodedString (base64)
certsDict = encodedCertsDictGen(certDirectory)

# upload files onto Mailchimp client
uploadsCounter = 1
for filename, encodedString in certsDict.items():
    print(str(uploadsCounter) + " uploading " + filename)
    client.files.create({"name": filename, "file_data": encodedString, "folder_id": certFolderID})
    print(str(uploadsCounter) + " " + filename + " upload complete")

    uploadsCounter = uploadsCounter +1

print("### Certificates upload process complete ###")


# ---------- Request, parse & organise cert file name & cert file URL details into dictionary ----------

# get file name & URL details of uploaded certificate PDFs (in raw JSON format):
certNamesURLs = client.files.all(get_all=True, fields="files.name,files.full_size_url")

# extract the 'files' dict[] from JSON;
# contains array of dictionaries, where each dictionary = file object
dictsArr = certNamesURLs["files"]

# initialise new dict to store keys=fileName (emails) & values=URLs
namesURLsDict = {}
for dict in dictsArr:
    email = dict["name"]
    CertURL = dict["full_size_url"]
    namesURLsDict[email] = CertURL
#print("namesURLsDict = \n", namesURLsDict)

print("### Certs file name & URL parse complete ###")

# ---------- Match & Assign Certificate URLs to Members by email address ----------

# for each email:URL entry, search members for email match,

assignmentCounter = 1
for pdfName, CertURL in namesURLsDict.items():

    # convert pdf name to email by removing '.pdf' suffix
    email = ""
    if pdfName.endswith(".pdf"):
        email=pdfName[:-4]
    else:
        #raise Exception("Incorrect Suffix found on pdfName " + pdfName)
        print( str(assignmentCounter) + " " + "#### Incorrect Suffix found on pdfName " + pdfName + " ####")
        continue

    # Query MailChimp API to see if there are any audience members with matching email address:
    responseEmailMatchQuery = client.search_members.get(get_all=True, query=email, fields="exact_matches.members.email_address")
    #prettyPrintJSONDict(responseEmailMatchQuery)

    # create array of matching emails from query:
    arrOfMatchesEmail = responseEmailMatchQuery["exact_matches"]["members"]
    emailMatchesArr = []
    for emailDict in arrOfMatchesEmail:
        matchedEmail = emailDict["email_address"]
        emailMatchesArr.append(matchedEmail)

    print( str(assignmentCounter) + " emailMatchesArr for " + email + " = ", emailMatchesArr)

    # assign cert URL to audience member with matching email address:
    if len(emailMatchesArr) > 0:
        if len(emailMatchesArr) > 1:
            print( str(assignmentCounter) + " " + "#### Duplicate emails detected, update administered for only one of the duplicates ####")

        subHashEmail = subHashGen(email)

        # update member info with new MMERGE6 merge field value (i.e. Cert URL):                                        #######
        client.lists.members.update(audienceID, subHashEmail, {"merge_fields": {mergeFieldName: CertURL}})              ####### Edit Merge Field name if necessary
        print( str(assignmentCounter) + " " + email + " CertURL added")

        # activate "hasCert" tag for this member:
        client.lists.members.tags.update(audienceID, subHashEmail, {"tags": [{"name": "hasCert", "status": "active"}]})
        print( str(assignmentCounter) + " " +email + " hasCert tag activated")

    else:
        print( str(assignmentCounter) + " " + "#### No matches for " + email + " ####")
        # occurs when certificate name does not correspond to an email address in the MailChimp system
        continue

    assignmentCounter = assignmentCounter + 1

print("### URL Assignment Process Complete ###")

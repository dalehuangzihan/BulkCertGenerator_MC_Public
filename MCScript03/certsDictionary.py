import os
import base64
import json

def encodedCertsDictGen(certDirectory):
    certsDict = {}

    counter = 0;
    for filename in os.listdir(certDirectory):
        if filename.endswith(".pdf"):
            fullPath = certDirectory + "/" + filename
            #print(fullPath)

            # generate base64 string from pdf file
            with open(fullPath, "rb") as pdf_file:
                encodedBytes = base64.b64encode(pdf_file.read())
            encodedString = encodedBytes.decode("utf-8")

            print( str(counter) + " " + filename + " encoding complete")

            # add filename - encodedString key value pair to dictionary
            certsDict[filename] = encodedString

        else:
            print("#### Skipped " + filename + " due to incorrect file format ####")

        counter = counter+1

    print("### batch encoding complete ###")
    return certsDict

# function to pretty-print json dictionaries
def prettyPrintJSONDict(jsonDict):
    print(json.dumps(jsonDict,indent=4,sort_keys=True,separators=(',',':')))
    return
import os
from mailchimp3 import MailChimp
from consts import *
from certsDictionary import *
from subscriberHash import subHashGen

client = MailChimp(mc_api = apiKey, mc_user = username, timeout=10.0)


certNamesURLs = client.files.all(get_all=True)
prettyPrintJSONDict(certNamesURLs)

pingFolderID = client.folders.all(get_all=True)
prettyPrintJSONDict(pingFolderID)
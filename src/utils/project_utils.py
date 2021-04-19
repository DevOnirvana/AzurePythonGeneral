import json
import time
import os
import sys
import logging
from azure.identity import ManagedIdentityCredential

logger = logging.getLogger(__name__)
logger.setLevel(logging.getLevelName(os.environ.get('logLevel', 'DEBUG')))
handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)


# parse email address 
def getEmailFromArn(*args): 
    raise NotImplementedError
 
 # load account info 
def getAccountInfo(*args):
    raise NotImplementedError

# load exception info from db
def getRuleConfigurations(*args):
    raise NotImplementedError

# get AWS client in target account
def getAzureClient(*args): 
    raise NotImplementedError  
#get bearer token
def authenticate():
    client_id = os.environ.get('client_id')
    credential_object = ManagedIdentityCredenial(client_id)
    token = credential_object.get_token("https://management.azure.com/.default")
    logging.info(token)
    return token
    

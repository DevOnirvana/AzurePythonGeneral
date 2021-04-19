'''
This function makes the bucket private by turning off the account public access
'''
#standard imports
import json
import logging
import os
import sys
import re
import datetime
import time
import requests
import azure.functions as func #requires package azure-functions
from azure.identity import ManagedIdentityCredential
#custom imports
from src.utils import product_utils
from src.utils import project_EventHandler


logger = logging.getLogger(__name__)
logger.setLevel(logging.getLevelName(os.environ.get('logLevel', 'DEBUG')))
handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.getLevelName(os.environ.get('logLevel', 'DEBUG')))
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)


def parseEvent(event, context):
    '''This function extracts information captured in event and sends the information to function
        doHandleEvent'''
    try:
        logger.info(event)
        eventScope = event['data']['authorization']['scope']
        resource = event['data']['authorization']['resource']
        doHandleEvent(eventScope, resource)

    except Exception as e:
        logger.error(f"Caught an unexpected error: {str(e)}")


def doHandleEvent(scope, resource):
    '''This function calls the class with arguments extracted from event which assume role, extract information
       from db and decide whether the remediation to be performed or not '''
    try:
        handler = ProjectventHandlerAzureStorageAccountAccess(scope, resource)
        return handler.handleEvent()
    except Exception as e:
        logger.error(f"Caught an unexpected error: {str(e)}")


class ProjectventHandlerAzureStorageAccountAccess(ProjectEventHandler.ProjectEventHandlerAzureService):


    def isRuleViolated(self):
        '''This functions checks whether the  bucket access is public or private, If public
        it returns true and proceeds with remediation'''
        '''make get request to fetch storage account properties'''
        try:
            storage_url = "https://management.azure.com" + self.scope
            client_id = project_utils.getAzureClient()
            bearer_token = project_utils.authenticate(client_id)
            response = requests.get(storage_url, params = {'api-version':'2019-06-01'}, headers = {"Authrorization" : "Bearer %s", bearer_token})
            data = json.loads(response.get_json())
            #check if rule violated
            if data['properties']['allowBlobPublicAccess'] is True:
                return True
            else:
                logging.info("Blob access is already private.")
                pass
        except Exception as e:
            logger.error(f"Caught an unexpected error: {str(e)}")


    def remediate(self):
        '''This function disables the storage account public access functionality of the bucket and
        makes the bucket priavte'''
        try:
            #make patch request to storage account
            result = {
                "properties": {
                    "allowBlobPublicAccess": False
                }
            }
            storage_url = "https://management.azure.com" + self.scope
            client_id = project_utils.getAzureClient()
            bearer_token = project_utils.authenticate(client_id)
            response = requests.post(storage_url, params = {'api-version':'2019-06-01'}, headers = {"Authrorization" : "Bearer %s", bearer_token}, json = result )
            logging.info(response.get_json())
            #return status code
            if response.status_code is 200:
                logging,info("Processed request succesfully")
        except Exception as e:
            logger.error(f"Caught an unexpected error: {str(e)}")


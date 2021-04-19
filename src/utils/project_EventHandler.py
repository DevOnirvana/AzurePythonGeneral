import json
import logging
import os
import sys
from datetime import datetime
from src.utils import project_utils

logger = logging.getLogger(__name__)
logger.setLevel(logging.getLevelName(os.environ.get('logLevel', 'DEBUG')))
handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

class ProjectEventHandler:
        
    def __init__(self, scope, resource):
        self.scope = scope
        self.resource = resource
        self.client = self.getClient() 
        self.accountInfo = self.getAccountRuleConfigurations() 
        self.ruleConfiguration = self.getRuleConfiguration()

    def handleEvent(self): 
        try:
            logger.debug("handling event....")
            if self.isRuleViolated():
                self.handleViolation()
        except Exception as e:
            logger.error(f"Caught an unexpected error: {str(e)}") 
             
    def getRuleConfiguration(self):  
        #returns a json of the rule configurations
        raise NotImplementedError
    
    def getAccountRuleConfigurations(self):
        raise NotImplementedError

    def getClient(self):
        raise NotImplementedError

    def isRuleViolated(self):
        raise NotImplementedError
    
    def handleViolation(self):
        raise NotImplementedError

    def remediate(self):
        raise NotImplementedError

    def createViolationEvent(self, *args):
        raise NotImplementedError

    def getEventPayload(self):
        raise NotImplementedError


class ProjectEventHandlerAzure(ProjectEventHandler):

    def getClient(self):
        try:
            logger.debug("getting client...")
            return project_utils.getAzureClient()
        except Exception as e:
            logger.error(f"Caught an unexpected error: {str(e)}")
            
    def getAccountInfo(self):
        try:
            logger.debug("getting account info...")
            return project_utils.getAccountInfo()
        except Exception as e:
            logger.error(f"Caught an unexpected error: {str(e)}")
            
    def getAccountRuleConfigurations(self):
        try:
            logger.debug("getting rule config...")
            return project_utils.getRuleConfigurations()
        except Exception as e:
            logger.error(f"Caught an unexpected error: {str(e)}")
    
    def handleViolation(self):
        try:
            json.dumps(self.ruleConfiguration,indent=4)
            remediationEnabled = self.ruleConfiguration['remediationsEnabled']
            logger.info(remediationEnabled)
            alertsEnabled = self.ruleConfiguration['alertsEnabled']
            #remediate event if needed
            if remediationEnabled: 
                self.remediate()
            self.createViolationEvent(remediationEnabled,alertsEnabled)
        except Exception as e:
            logger.error(f"Caught an unexpected error: {str(e)}")

class ProjectventHandlerAzureService(ProjectEventHandlerAzure):

    def __init__(self, scope, resource):
        super().__init__(self, scope, resource)


    def getEventPayload(self):
        try:
            eventInfo = {
                'resourceName': self.resource
            }
            return eventInfo
        except Exception as e:
            logger.error(f"Caught an unexpected error: {str(e)}")
        
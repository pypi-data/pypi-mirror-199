import os
import boto3
import requests
from tkaws import Tkkinesis

class Tkauditlogs():

    def put_mongo_log(self, old_data, new_data, username):
        audit_log = dict()
        audit_log['old_image'] = old_data
        audit_log['new_image'] = new_data
        audit_log['username'] = username
        audit_log['source'] = 'mongo'
        # Tkkinesis().put_record(audit_log)
        audit_url = self.get_audit_url()
        requests.post(audit_url, json=audit_log)
        return True

    def put_elastic_search_log(self, old_data, new_data, username):
        audit_log = dict()
        audit_log['old_image'] = old_data
        audit_log['new_image'] = new_data
        audit_log['username'] = username
        audit_log['source'] = 'elastic_search'
        Tkkinesis().put_record(audit_log)
        return True

    def get_kinesis(self):
        env = os.getenv("ENV")
        project = os.getenv("PROJECT")
        return True
    def get_audit_url(self):
        self.project = os.getenv("PROJECT") # MAP, CMS , LND
        URL_STRUCTURE= f"/v2/api/audit_log/{self.project}"
        return URL_STRUCTURE






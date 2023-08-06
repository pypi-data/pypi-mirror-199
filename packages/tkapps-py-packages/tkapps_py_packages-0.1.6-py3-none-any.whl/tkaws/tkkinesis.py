import os
import boto3
import json

class Tkkinesis():
    def __init__(self, region=None):
        """
        :param region: The region for AWS Athena
        """
        self.service_name = 'kinesis'
        if region is None:
            region = os.getenv("KINESIS_REGION")
        if region is None:
            region = os.getenv("REGION")
        if region is None:
            raise ValueError("REGION is missing in both ENV Variable and constructor params.")
        self.region = region
        self.env = os.getenv("ENV")
        self.kinesis_stream = os.getenv("KINESIS_STREAM")
        self.access_key = os.getenv("AWS_ACCESS_KEY_ID")
        self.secret_key = os.getenv("AWS_SECRET_ACCESS_KEY")
        self.http_timeout = 60

    def get_client(self):
        """
        To be used internally for the purpose of creating the boto3 client of athena.
        This method creates the boto3 client for AWS, The client can later be accessed using 'self.client'
        :return: Self object
        """
        if self.access_key is None or self.secret_key is None:
            self.client = boto3.client(service_name=self.service_name, region_name=self.region)
        else:
            self.client = boto3.client(service_name=self.service_name, region_name=self.region,
                                       aws_access_key_id=self.access_key, aws_secret_access_key=self.secret_key)
        return self

    def get_resource(self):
        """
        To be used internally for the purpose of creating the boto3 resource of athena.
        This method creates the boto3 resource for AWS, The resource can later be accessed using 'self.resource'
        :return: Self object
        """
        if self.access_key is None or self.secret_key is None:
            self.resource = boto3.resource(service_name=self.service_name, region_name=self.region)
        else:
            self.resource = boto3.resource(service_name=self.service_name, region_name=self.region,
                                           aws_access_key_id=self.access_key, aws_secret_access_key=self.secret_key)
        return self

    def put_records(self, records):
        """
        :param records: Insert multiple records to Kinesis at the same time (in on go).
        :return:
        """
        self.get_client()
        try:
            self.client.put_records(StreamName=self.kinesis_stream, Records=records)
            return True
        except Exception as err:
            print(err)
            return False


    def put_record(self, record):
        """
        :param record: Insert single record to Kinesis.
        :return:
        """
        self.get_client()
        try:
            self.client.put_record(StreamName=self.kinesis_stream, Data=json.dumps(record), PartitionKey=record["log_timestamp"])
            return True
        except Exception as err:
            print(err)
            return False

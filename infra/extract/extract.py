import requests
import json
import boto3
from infra.logger.logger import logging

def extract_api(path: str, api_key: str = None):
    try:
        if api_key:
            header = {'x-apisports-key': api_key}

        else:
            header = {}

        response = requests.get(path, headers=header)
        data = response.json()
        logging.info('Successfully requested data')

        return data
    
    except Exception as e:
        logging.error('Fatally errored in requesting data')
        raise e

def store_to_s3_bronze(data, bucket_name: str, key: str):
    try:
        s3 = boto3.client('s3')
        logging.info('Established connection to S3')

        s3.put_object(
            Bucket=bucket_name,
            Key=key,
            Body=json.dumps(data)
        )
        logging.info('Successfully stored data to s3')

    except Exception as e:
        logging.error(f'Fatally errored in Loading data into S3 bucket')
        raise e
    
if __name__ == '__main__':
    pass
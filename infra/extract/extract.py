import requests
import json
import boto3
from infra.logger.logger import logging

def extract_api(path: str, api_key: str = None, params: dict = {}):
    try:
        if api_key:
            header = {'x-apisports-key': api_key}

        else:
            header = {}

        response = requests.get(path, headers=header, params = params)

        if response.status_code != 200:
            logging.error(f"API call failed: {response.status_code} - {response.text[:200]}")
            raise requests.HTTPError(f"Non-200 response: {response.status_code}")

        data = response.json().get('response')

        if not data:
            logging.warning('API returned null')

        logging.info('Successfully requested data')

        return {'status_code': response.status_code, 'data': data}
    
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
    
def load_from_s3_bronze(bucket_name: str, key: str):
    s3 = boto3.client('s3')
    logging.info('Established connection to S3')
    obj = s3.get_object(Bucket=bucket_name,
                        key=key)
    
    logging.info('Successfully loaded JSON data')
    return json.loads(obj['Body'].read())

if __name__ == '__main__':
    pass
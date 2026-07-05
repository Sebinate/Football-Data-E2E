import os

from infra import extract
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

AWS_BUCKET_NAME = os.getenv('AWS_S3_BUCKET_NAME')

FOOTBALL_API_KEY = os.getenv('FOOTBALL_API_KEY')
FOOTBALL_API_HOST = os.getenv('FOOTBALL_API_HOST')

test_call = 'leagues'

test_url = f'{FOOTBALL_API_HOST}/{test_call}'

data = extract.extract_api(test_url, FOOTBALL_API_KEY)
key = f'api_football/{test_call}/load_date={datetime.today().strftime("%Y-%m-%d")}/{test_call}_data.json'

extract.store_to_s3_bronze(data, AWS_BUCKET_NAME, key = key)
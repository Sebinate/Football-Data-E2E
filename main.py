import os

from infra import extract
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

AWS_BUCKET_NAME = os.getenv('AWS_S3_BUCKET_NAME')

FOOTBALL_API_KEY = os.getenv('FOOTBALL_API_KEY')
FOOTBALL_API_HOST = os.getenv('FOOTBALL_API_HOST')

test_call_1 = 'leagues'

test_url_1 = f'{FOOTBALL_API_HOST}/{test_call_1}'

data_1 = extract.extract_api(test_url_1, FOOTBALL_API_KEY)
key_1 = f'api_football/{test_call_1}/load_date={datetime.today().strftime("%Y-%m-%d")}/{test_call_1}_data.json'

extract.store_to_s3_bronze(data_1, AWS_BUCKET_NAME, key = key_1)

#######
test_call_2 = 'teams'

test_url_2 = f'{FOOTBALL_API_HOST}/{test_call_2}'

data_2 = extract.extract_api(test_url_2, FOOTBALL_API_KEY, params = {'season': '2022', 'league': 39})
key_2 = f'api_football/{test_call_2}/load_date={datetime.today().strftime("%Y-%m-%d")}/{test_call_2}_data.json'

extract.store_to_s3_bronze(data_2, AWS_BUCKET_NAME, key = key_2)

#######
test_call_3 = 'fixtures'

test_url_3 = f'{FOOTBALL_API_HOST}/{test_call_3}'

data_3 = extract.extract_api(test_url_3, FOOTBALL_API_KEY, params = {'season': '2022', 'league': 39})
key_3 = f'api_football/{test_call_3}/load_date={datetime.today().strftime("%Y-%m-%d")}/{test_call_3}_data.json'

extract.store_to_s3_bronze(data_3, AWS_BUCKET_NAME, key = key_3)
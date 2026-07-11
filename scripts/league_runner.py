from infra.extract import extract
from datetime import datetime
import os

# Under documentation the recommended api call is 1 per day, considering that we are simply focusing on the preimer league, we will udpate this every year (new season)

def fetch_league():
    FOOTBALL_API_KEY = os.getenv('FOOTBALL_API_KEY')
    FOOTBALL_API_HOST = os.getenv('FOOTBALL_API_HOST')
    AWS_BUCKET_NAME = os.getenv('AWS_S3_BUCKET_NAME')

    target = 'leagues'

    url = f"{FOOTBALL_API_HOST}/{target}"
    response = extract.extract_api(path=url,
                                   api_key=FOOTBALL_API_KEY,
                                   )
    
    key = f'api_football/{target}/load_date={datetime.today().strftime("%Y-%m-%d")}/{target}_data.json'

    extract.store_to_s3_bronze(data=response,
                               bucket_name=AWS_BUCKET_NAME,
                               key=key)

if __name__ == "__main__":
    fetch_league()
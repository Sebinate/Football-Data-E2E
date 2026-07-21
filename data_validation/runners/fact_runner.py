from infra.extract import store_to_s3_bronze
from data_validation.expectations import validate_kept_columns_fixture, validate_helper
from dotenv import load_dotenv
import sys
from datetime import datetime
import os

def main():
    load_dotenv()

    AWS_S3_BUCKET_NAME = os.getenv('AWS_S3_BUCKET_NAME')

    if len(sys.argv) > 1:
        season = sys.argv[1]
    else:
        season = "2022"

    results = validate_helper(validator=validate_kept_columns_fixture,
                    bucket_name=AWS_S3_BUCKET_NAME,
                    target='fixture',
                    execution_date=datetime.today().strftime("%Y-%m-%d"),
                    season=season)
    
    # Add functionality here to store the data into _validation
    store_to_s3_bronze(
        results,

    )
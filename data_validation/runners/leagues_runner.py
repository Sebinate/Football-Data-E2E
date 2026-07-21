from data_validation.expectations import validate_kept_columns_league, validate_helper
from infra.logger import log_result
from infra.extract import store_to_s3_bronze
from dotenv import load_dotenv
from datetime import datetime
import sys
import os

def main():
    load_dotenv()

    AWS_S3_BUCKET_NAME = os.getenv('AWS_S3_BUCKET_NAME')
    execution_date=datetime.today().strftime("%Y-%m-%d")

    #For leagues
    results = validate_helper(validator=validate_kept_columns_league,
                                      bucket_name=AWS_S3_BUCKET_NAME,
                                      target='leagues',
                                      execution_date=execution_date,
                                      season=None)

    store_to_s3_bronze(
        data=results,
        bucket_name=AWS_S3_BUCKET_NAME,
        key=f'_validation_results/{results["suite"]}/{results["execution_date"]}.json'
    )

    log_result(results)

    if not results['passed']:
        sys.exit(1)

if __name__ == "__main__":
    main()
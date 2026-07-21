from data_validation.expectations import validate_kept_columns_teams, validate_helper
from infra.logger import log_result
from infra.extract import store_to_s3_bronze
from dotenv import load_dotenv
from datetime import datetime
import sys
import os

def main():
    load_dotenv()

    AWS_S3_BUCKET_NAME = os.getenv('AWS_S3_BUCKET_NAME')

    results = validate_helper(validator=validate_kept_columns_teams,
                                    bucket_name=AWS_S3_BUCKET_NAME, 
                                    target='teams', 
                                    execution_date=datetime.today().strftime('%Y-%m-%d'), 
                                    season=None)

    store_to_s3_bronze(
        data=results,
        bucket_name=AWS_S3_BUCKET_NAME,
        key=f'_validation_results/{results["suite"]}/{results["execution_date"]}.json'
    )

    log_result(results)

    if not results["passed"]:
        sys.exit(1)

if __name__ == "__main__":
    main
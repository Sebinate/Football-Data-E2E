from data_validation.expectations import validate_kept_columns_league, validate_kept_columns_teams, validate_helper
from dotenv import load_dotenv
from datetime import datetime
import os

load_dotenv()

AWS_S3_BUCKET_NAME = os.getenv('AWS_S3_BUCKET_NAME')

#For leagues
validate_helper(validator=validate_kept_columns_league,
                bucket_name=AWS_S3_BUCKET_NAME,
                target='leagues',
                execution_date=datetime.today().strftime("%Y-%m-%d"),
                season=None)

#For teams
validate_helper(validator=validate_kept_columns_teams,
                bucket_name=AWS_S3_BUCKET_NAME,
                target='teams',
                execution_date=datetime.today().strftime("%Y-%m-%d"),
                season=None)

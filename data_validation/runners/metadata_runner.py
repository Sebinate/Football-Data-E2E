from infra.extract import load_from_s3_bronze
from data_validation.expectations import validate_raw_shape, validate_kept_columns_league, validate_kept_columns_teams
import sys
import datetime

if len(sys.argv) > 1:
    season = sys.argv[1]
else:
    season = "2022"

def validate_league(execution_date: str) -> dict:
    data = load_from_s3_bronze(execution_date) # Turn execution_date to key

    shape_errors = validate_raw_shape(data)
    if shape_errors:
        return {
            "suite": "fixtures_scores",
            "execution_date": execution_date,
            "passed": False,
            "stage": "raw_shape",
            "errors": shape_errors,
            "timestamp": datetime.utcnow().isoformat(),
        }

    ge_result = validate_kept_columns_league(data)
    return {
        "suite": "fixtures_scores",
        "execution_date": execution_date,
        "passed": ge_result.success,
        "stage": "column_validation",
        "errors": [] if ge_result.success else ge_result.to_json_dict()["results"],
        "timestamp": datetime.utcnow().isoformat(),
    }

def validate_teams(execution_date: str) -> dict:
    data = load_from_s3_bronze(execution_date) # Turn execution_date to key

    shape_errors = validate_raw_shape(data)
    if shape_errors:
        return {
            "suite": "fixtures_scores",
            "execution_date": execution_date,
            "passed": False,
            "stage": "raw_shape",
            "errors": shape_errors,
            "timestamp": datetime.utcnow().isoformat(),
        }

    ge_result = validate_kept_columns_teams(data)
    return {
        "suite": "fixtures_scores",
        "execution_date": execution_date,
        "passed": ge_result.success,
        "stage": "column_validation",
        "errors": [] if ge_result.success else ge_result.to_json_dict()["results"],
        "timestamp": datetime.utcnow().isoformat(),
    }

if __name__ == "__main__":
    pass
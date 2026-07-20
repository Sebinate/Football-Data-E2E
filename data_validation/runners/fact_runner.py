from infra.extract import load_from_s3_bronze
from data_validation.expectations import validate_raw_shape, validate_kept_columns_fixture
import datetime

def validate_fixture(execution_date: str) -> dict:
    data = load_from_s3_bronze(execution_date)

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

    ge_result = validate_kept_columns_fixture(data)
    return {
        "suite": "fixtures_scores",
        "execution_date": execution_date,
        "passed": ge_result.success,
        "stage": "column_validation",
        "errors": [] if ge_result.success else ge_result.to_json_dict()["results"],
        "timestamp": datetime.utcnow().isoformat(),
    }
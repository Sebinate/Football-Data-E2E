from infra.extract import load_from_s3_bronze
from datetime import datetime, timezone

def validate_raw_shape(data: list, batch_size: int = 500):
    errors = []

    if not isinstance(data, list):
        errors.append(f"Expected a list of records, got {type(data)}")
        return errors

    if len(data) == 0:
        errors.append("Empty record list — no fixtures returned")
    elif len(data) > batch_size:
        errors.append(f"Unexpectedly large record count: {len(data)}")

    return errors

def validate_helper(validator, bucket_name:str, target: str, execution_date: str, season: str = None):
    # Just to be robust
    execution_date = execution_date.strftime("%Y-%m-%d")

    key = f'api-football/{target}/load_date={execution_date}/{target}_data_{'' if not season else '_'}{'' if not season else season}.json'
    data = load_from_s3_bronze(bucket_name=bucket_name,
                               key=key) # Turn execution_date to key

    shape_errors = validate_raw_shape(data)
    if shape_errors:
        return {
            "suite": target,
            "execution_date": execution_date,
            "passed": False,
            "stage": "raw_shape",
            "errors": shape_errors,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

    ge_result = validator(data)
    return {
        "suite": target,
        "execution_date": execution_date,
        "passed": ge_result.success,
        "stage": "column_validation",
        "errors": [] if ge_result.success else ge_result.to_json_dict()["results"],
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }

if __name__ == "__main__":
    pass
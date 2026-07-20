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
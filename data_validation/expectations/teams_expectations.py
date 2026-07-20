import pandas as pd
import great_expectations as gx

def validate_kept_columns_teams(data: list):
    KEPT_FIELDS = [
        "team.id",
        "team.name",
        "team.code",
        "team.logo",
        "venue.id",
        "venue.name",
        "venue.address",
        "venue.city",
        "venue.capacity",
        "venue.surface"
    ]

    df = pd.json_normalize(data)[KEPT_FIELDS]

    context = gx.get_context()
    validator = context.sources.pandas_default.read_dataframe(df)

    validator.expect_column_values_to_not_be_null("team.id")
    validator.expect_column_values_to_be_unique("team.id")
    validator.expect_column_values_to_not_be_null("team.code")
    validator.expect_column_values_to_not_be_null("team.logo")
    validator.expect_column_values_to_be_unique("venue.id")
    validator.expect_column_values_to_not_be_null("venue.id")
    validator.expect_column_values_to_not_be_null("venue.name")
    validator.expect_column_values_to_not_be_null("venue.city")
    validator.expect_column_values_to_be_between("venue_capacity", min_value=0, max_value=500_000, mostly=0.99)

    return validator.validate()
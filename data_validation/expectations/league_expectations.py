import pandas as pd
import great_expectations as gx

def validate_kept_columns_league(data: list):
    KEPT_FIELDS = [
        "league.id",
        "league.name",
        "league.type",
        "league.logo",
        "country.name",
        "country.code",
        "country.flag"
    ]

    df = pd.json_normalize(data)[KEPT_FIELDS]

    context = gx.get_context()
    validator = context.sources.pandas_default.read_dataframe(df)

    validator.expect_column_values_to_not_be_null("league.id")
    validator.expect_column_values_to_be_unique("league.id")
    validator.expect_column_values_to_not_be_null("league.type")
    validator.expect_column_values_to_not_be_null("league.logo")
    validator.expect_column_values_to_not_be_null("country.code")
    validator.expect_column_values_to_be_unique("country.code")
    validator.expect_column_values_to_not_be_null("country.name")

    return validator.validate()
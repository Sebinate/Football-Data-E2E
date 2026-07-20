import pandas as pd
import great_expectations as gx

def validate_kept_columns_fixture(data: list):
    KEPT_FIELDS = [
        "fixture.id",
        "fixture.date",
        "fixture.venue.name",
        "status.short",
        "status.elapsed",
        "league.name",
        "league.season",
        "league.round",
        "teams.home.name",
        "teams.home.winner",
        "teams.away.name",
        "teams.away.winner",
        "goals.home",
        "goals.away",
        "score.halftime.home",
        "score.halftime.away",
    ]

    df = pd.json_normalize(data)[KEPT_FIELDS]

    context = gx.get_context()
    validator = context.sources.pandas_default.read_dataframe(df)

    validator.expect_column_values_to_not_be_null("fixture.id")
    validator.expect_column_values_to_be_unique("fixture.id")
    validator.expect_column_values_to_not_be_null("teams.home.name")
    validator.expect_column_values_to_not_be_null("teams.away.name")
    validator.expect_column_values_to_be_between("goals.home", min_value=0, max_value=20, mostly=0.99)
    validator.expect_column_values_to_be_between("goals.away", min_value=0, max_value=20, mostly=0.99)
    validator.expect_column_values_to_be_in_set(
        "status.short", ["NS", "1H", "HT", "2H", "FT", "PST", "CANC"]
    )

    return validator.validate()


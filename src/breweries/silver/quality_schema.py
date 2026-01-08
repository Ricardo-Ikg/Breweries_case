import pandera as pa
from pandera import Column, Check


BREWERIES_QUALITY_SCHEMA = pa.DataFrameSchema(
    {
        "id": Column(
            str,
            nullable=False,
            checks=[
                Check.str_length(min_value=1),
            ],
        ),

        "name": Column(
            str,
            nullable=False,
            checks=[
                Check.str_length(min_value=1),
            ],
        ),

        "brewery_type": Column(
            str,
            nullable=False,
            checks=[
                Check.isin(
                    [
                        "micro",
                        "nano",
                        "regional",
                        "brewpub",
                        "large",
                        "planning",
                        "bar",
                        "contract",
                        "proprietor",
                        "closed",
                    ]
                )
            ],
        ),

        "state": Column(
            str,
            nullable=False,
            checks=[
                Check.str_length(min_value=2),
            ],
        ),

        "country": Column(
            str,
            nullable=False,
            checks=[
                Check.equal_to("United States"),
            ],
        ),
    },
    strict=False,  # permite colunas extras
)

import pandas as pd
from rich.rule import Rule
from rich.text import Text
from pycake.data_provider import (
    default_data_provider,
    serve,
    extract_parquet_response,
    get_lang,
    get_cake_msg,
    console,
    cli_colors
)


def metadata(x, data_provider=default_data_provider(), lang=get_lang(), include_description=True):
    """Get metadata for an object.

    Examples
    --------
    >>> from pycake import get_address_features, metadata
    >>> adr_feat = get_address_features("Bundesstrasse 9 6003 Luzern")
    >>> metadata(adr_feat[["com_name", "com_canton", "bev_total"]])

    Parameters
    ----------
    x : pandas.DataFrame
        Object you want to get metadata for
    data_provider : object, optional
        An object of type `RemoteDataProvider` (see :class:`Datenbaecker`)
    lang : str
        Language for the metadata, default is `en`
    include_description : bool
        If True, include descriptions in the output. Default is `True`

    Returns
    -------
    None
        An invisible DataFrame with the metadata.

    """

    what = x["endpoint"].iloc[0]
    if what is None:
        raise ValueError(get_cake_msg("no_endpoint"))
    if what != "address-features":
        raise ValueError(get_cake_msg("no_metadata"))
    try:
        mdt = serve(f"{what}/metadata", data_provider, read_body_hook=extract_parquet_response)
    except Exception as e:
        raise RuntimeError(f"Failed to fetch metadata: {e}")
    if isinstance(x, pd.DataFrame):
        mdt = mdt[mdt['name'].isin(x.columns)]

    source_col = f"source_{lang}"
    if source_col not in mdt.columns:
        raise KeyError(f"Column '{source_col}' not found in metadata.")

    all_sources = sorted(mdt[source_col].unique())
    for src in all_sources:
        heading = Text(src, style=cli_colors["col_red"])
        console.print(Rule(heading, style="black"))

        curr_cols = mdt[mdt[source_col] == src].sort_values("name")
        for _, row in curr_cols.iterrows():
            print(f"\u2022 {row['name']}")
            if include_description:
                col_desc = row[[lang, "en", "de", "fr", "it"]].dropna().tolist()
                if col_desc:
                    print(col_desc[0])

import pandas as pd
from pycake.data_provider import default_data_provider, serve, extract_parquet_response


def get_cantonal_entities(dp=default_data_provider()):
    """Get Labels and ID for Cantonal Entities.

    Parameters
    ----------
    dp : object, optional
        An object of type `RemoteDataProvider` (see :class:`Datenbaecker`)

    Returns
    -------
    pandas.DataFrame
        A DataFrame with columns `id` and `label` containing the identifiers
        and labels from the office of federal statistics.

    See Also
    --------
    get_plz_entities : Get Labels and ID for Postal Code Entities.
    get_communal_entities : Get Labels and ID for Communal Entities.
    """
    sb = serve("geometries/cantons-shape.parquet", dp, read_body_hook=extract_parquet_response)
    sb = pd.DataFrame(sb)
    sb = sb[["bfs_num", "label", "name"]].sort_values("bfs_num").rename(columns={"bfs_num": "id"})
    return sb


def get_plz_entities(dp=default_data_provider()):
    """Get Labels and ID for Postal Code Entities.

    Parameters
    ----------
    dp : object, optional
        An object of type `RemoteDataProvider` (see :class:`Datenbaecker`)

    Returns
    -------
    pandas.DataFrame
        A DataFrame with columns `id` and `label` containing the identifiers
        and labels from the office of federal statistics.

    See Also
    --------
    get_cantonal_entities : Get Labels and ID for Cantonal Entities.
    get_communal_entities : Get Labels and ID for Communal Entities.
    """

    sb = serve("geometries/plz-shape.parquet", dp, read_body_hook=extract_parquet_response)
    sb = pd.DataFrame(sb)
    sb = sb[["plz"]].drop_duplicates().assign(id=lambda x: x["plz"])
    return sb[["id", "plz"]]


def get_communal_entities(dp=default_data_provider()):
    """Get Labels and ID for Communal Entities.

    Parameters
    ----------
    dp : object, optional
        An object of type `RemoteDataProvider` (see :class:`Datenbaecker`)

    Returns
    -------
    pandas.DataFrame
        A DataFrame with columns `id` and `label` containing the identifiers
        and labels from the office of federal statistics.

    See Also
    --------
    get_cantonal_entities : Get Labels and ID for Cantonal Entities.
    get_plz_entities : Get Labels and ID for Postal Code Entities.
    """

    sb = serve("geometries/communes-shape.parquet", dp, read_body_hook=extract_parquet_response)
    sb = pd.DataFrame(sb)
    sb = sb[["bfs_num", "name", "kanton_label"]].sort_values("bfs_num").rename(columns={"bfs_num": "id"}).drop_duplicates()
    return sb

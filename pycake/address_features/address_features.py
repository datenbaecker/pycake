from datetime import date
from pycake.data_provider import default_data_provider, serve, order_and_serve, extract_parquet_response


def get_address_features(addresses=None, data_provider=default_data_provider()):
    """Get analytical base table for Swiss addresses.

    Notes
    -----
    This function provides a set of variables for Swiss addresses.
    The data originates from different sources. You can call ``metadata()``
    on the DataFrame in order to get a description and the source of
    the data in the columns. If `None` is passed for the argument
    `addresses`, you get the data for a selected sample of Swiss
    addresses. If address strings are provided, the backend does a fuzzy
    matching with the addresses from the `official directory of
    building addresses <https://www.swisstopo.admin.ch/en/official-directory-of-building-addresses>`_
    from swisstopo.

    Examples
    --------
    >>> from pycake import get_address_features
    >>> adr_data = get_address_features("Bundesstrasse 9 6003 Luzern")

    Parameters
    ----------
    addresses : list of str, optional
        Either a list with address strings to search for or `None` for
        a standard address sample
    data_provider : object, optional
        An object of type `DataProvider`, If None, a default data
        provider is used

    Returns
    -------
    pandas.DataFrame
        A table with a battery of variables for the addresses.
    """

    if addresses is None:
        data = serve(
            "address-features/standard-dataset",
            data_provider,
            read_body_hook=extract_parquet_response,
            metadata_endpoint="address-features"
        )
    else:
        req_body = [{"full_address": addr, "date": str(date.today())} for addr in addresses]
        data = order_and_serve(
            "address-features",
            body_json=req_body,
            dp=data_provider,
            read_body_hook=extract_parquet_response,
            timeout=60
        )
    return data

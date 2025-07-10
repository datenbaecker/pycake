from datetime import date
from pycake.data_provider import default_data_provider, order_and_serve, extract_parquet_response


def search_companies(companies, data_provider=default_data_provider()):
    """Search for Swiss companies by name.

    Notes
    -----
    The function sends a request with the
    searched companies to the backend. The backend performs a fuzzy matching
    with the company name.

    Examples
    --------
    >>> from pycake import search_companies
    >>> company_info = search_companies("Datenbäcker GmbH")

    Parameters
    ----------
    companies : list of str
        List of company names to search for
    data_provider : object, optional
        An object of type `DataProvider`, If None, a default data
        provider is used

    Returns
    -------
    dict
        A dictionary containing three DataFrames:
        - `company_details`: A table with information for the searched
        companies (legal form, address, etc.)
        - `related_companies`: A table with related companies for the
        search companies
        - `company_person`: A table with persons related to the search companies
    """

    req_body = [{"company_name": company, "date": str(date.today())} for company in companies]

    data = order_and_serve(
        "company-search",
        body_json=req_body,
        dp=data_provider,
        read_body_hook=extract_parquet_response,
        timeout=120
    )

    return {"company_details": data[0],
            "related_companies": data[1],
            "company_person": data[2]}

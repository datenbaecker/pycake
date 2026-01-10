import os
import time
import requests
from .utils import download_cake
from .message import get_cake_msg
from .theme import cake_progress_bar


def serve(what, dp, read_body_hook=lambda x: x, alert_download=True, metadata_endpoint=None, **kwargs):
    """Get Data from a Data Provider. Depending on the type of
    `DataProvider` and the settings, `serve` might return cached data
    from memory or disk. If the data does not exist locally, a
    `RemoteDataProvider` might download the data from the internet and
    saves is to the cache folder on the disk depending on the settings
    (see :class:`Datenbaecker`).

    Parameters
    ----------
    what : str
        Name of the data source
    dp : object
        An object of type `RemoteDataProvider` (see :class:`Datenbaecker`)
    read_body_hook : callable, optional
        A function to process the response body, defaults to identity function
    metadata_endpoint : str, optional
        The endpoint metadata to tag the results with
    **kwargs : dict
        Further parameter (currently not used)

    Returns
    -------
    pandas.DataFrame
        The requested data.
    """

    what = f"{dp.api_version_prefix}{what}"
    if dp.host is not None:
        try:
            dt = dp.cache.get(what)
        except ValueError:
            dt = None
        if dt is None:
            dt = download_cake(dp, what, read_body_hook=read_body_hook, alert_download=alert_download)
            dp.cache.add(dt, what)
        if metadata_endpoint is not None:
            dt["endpoint"] = metadata_endpoint
        else:
            dt["endpoint"] = what
        return dt
    else:
        return dp.cache.get(what)


def order_and_serve(what, body_json, dp, read_body_hook=lambda x: x, metadata_endpoint=None, timeout=60):
    """Get Data from a Data Provider. Depending on the type of `DataProvider`
    and the settings, `serve` might return cached data from memory or disk.
    If the data does not exist locally, a `RemoteDataProvider` might download
    the data from the internet and saves is to the cache folder on the disk
    depending on the settings (see :class:`Datenbaecker`).

    Parameters
    ----------
    what : str
        Name of the data source
    body_json : dict
        The JSON body containing the request parameters.
    dp : object
        An object of type `RemoteDataProvider` (see :class:`Datenbaecker`)
    read_body_hook : callable, optional
         A function to process the response body, defaults to identity function
    metadata_endpoint : str, optional
        The endpoint metadata to tag the results with
    timeout : int
        Timeout in seconds for the request, defaults to 60 seconds

    Returns
    -------
    pandas.DataFrame
        The requested data. If multiple results are returned, a list of
        DataFrames is returned.
    """
    url = os.path.join(dp.host, f"{dp.api_version_prefix}{what}")

    response = requests.post(
        url,
        params={"format": "parquet"},
        json=body_json,
        timeout=timeout
    )
    response.raise_for_status()
    post_res = response.json()

    start_time = time.time()
    prog_steps = 10

    res_ready = False
    ctr = 0
    update_progress = cake_progress_bar(prog_steps, style="cake")
    try:
        while not res_ready:
            time.sleep(0.5)
            if time.time() - start_time > timeout:
                raise TimeoutError(get_cake_msg("timeout"))
            if ctr < prog_steps:
                update_progress(ctr + 1)
            if ctr % 2 == 0:
                task_url = os.path.join(url, post_res["taskId"])
                task_res = requests.get(task_url)
                task_res.raise_for_status()
                task_status = task_res.json()
                res_ready = task_status["status"] == "completed"
            ctr += 1
    finally:
        update_progress(prog_steps)
        print()

    res_urls = task_status["result"]["url"]
    if isinstance(res_urls, str):
        res_urls = [res_urls]
    results = []
    for res in res_urls:
        res_url = requests.get(res)
        data = read_body_hook(res_url)
        data["endpoint"] = metadata_endpoint or what
        results.append(data)
    if len(results) == 1:
        results = results[0]
    return results

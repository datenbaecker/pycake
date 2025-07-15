import os
import io
import gzip
import pickle
import requests
import tempfile
import pandas as pd
from .data_provider import RemoteDataProvider
from .message import get_cake_msg, cake_alert_info


def extract_parquet_response(res):
    file_conn = io.BytesIO(res.content)
    return pd.read_parquet(file_conn)


def download_cake(dp, what, read_body_hook=lambda x: x, alert_download=True):

    if not isinstance(dp, RemoteDataProvider):
        raise TypeError(get_cake_msg("abort_class", expected=RemoteDataProvider, argument="dp"))

    url = os.path.join(dp.host, what)
    print_debug(f"Downloading from {url}")
    if alert_download:
        cake_alert_info("downloading")
    res = requests.get(url)
    res.raise_for_status()

    return read_body_hook(res)


def set_log_level(log_level="prod"):

    current_log_level = log_level

    def log_level_manager(new_level=None):
        nonlocal current_log_level
        if new_level is not None:
            if new_level not in ["prod", "debug"]:
                raise ValueError("Log level must be 'prod' or 'debug'")
            current_log_level = new_level
        return current_log_level

    return log_level_manager


log_level = set_log_level()


def print_debug(*args):
    if log_level() == "debug":
        print(*args)



# def extract_swiss_boundaries(res):
#     with gzip.open(res, 'rb') as f:
#         return f.read()


# def extract_pickle_response(res):
#     obj = res.content
#     with tempfile.NamedTemporaryFile(suffix=".pkl", delete=False) as temp_file:
#         temp_file.write(obj)
#         temp_file_path = temp_file.name
#     with open(temp_file_path, "rb") as f:
#         return pickle.load(f)
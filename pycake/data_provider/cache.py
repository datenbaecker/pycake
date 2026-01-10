import os
import sys
import time
import pickle
import appdirs
from pathlib import Path
from .message import cake_alert, cake_alert_info


class InMemoryCache:
    def __init__(self):
        self._cached_data = [None] * 1000
        self._names = [""] * 1000

    def get(self, name):
        if self.exists(name):
            idx = self._names.index(name)
            return self._cached_data[idx]
        return None

    def exists(self, name):
        return name in self._names

    def add(self, obj, name, overwrite=False):
        if not self.exists(name) or overwrite:
            try:
                idx = self._names.index("")
            except ValueError:
                raise RuntimeError("Max data cache size reached")
            self._cached_data[idx] = obj
            self._names[idx] = name

    def clean_cache(self):
        self._cached_data = [None] * 1000
        self._names = [""] * 1000


class FileCache(InMemoryCache):
    def __init__(self, cache_dir):
        super().__init__()
        self._cache_dir = os.path.join(os.path.abspath(cache_dir), "cake_storage")
        os.makedirs(self._cache_dir, exist_ok=True)

    def get(self, name):
        data = super().get(name)
        if data is None and self.exists(name):
            data = self._load_file(name)
            super().add(data, name)
        return data

    def exists(self, name):
        file_path = self._get_filepath(name)
        return super().exists(name) or os.path.exists(file_path)

    def add(self, obj, name, overwrite=False):
        if not self.exists(name) or overwrite:
            super().add(obj, name, overwrite)
            self._save_file(obj, name)

    def clean_cache(self):
        super().clean_cache()
        for file in Path(self._cache_dir).glob("*"):
            file.unlink()

    def cache_directory(self):
        return self._cache_dir

    def _get_filepath(self, name):
        return os.path.join(self._cache_dir, f"{name}.pkl")

    def _load_file(self, name):
        file_path = self._get_filepath(name)
        with open(file_path, "rb") as f:
            return pickle.load(f)

    def _save_file(self, obj, name):
        file_path = self._get_filepath(name)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "wb") as f:
            pickle.dump(obj, f)


def ask_cache_data():
    cake_alert_info("info_cache_data")
    cake_alert("cache_data")
    sys.stdout.flush()
    time.sleep(0.5)
    while True:
        answer = input().strip().lower()
        if answer in ["j", "y", "n"]:
            break
        cake_alert("cache_data")
        sys.stdout.flush()
        time.sleep(0.5)
    return {"j": True, "y": True, "n": False}[answer]


def ask_delete_cache(cache_dir):
    cake_alert("delete_cache_data", cache_data_path=cache_dir)
    sys.stdout.flush()
    time.sleep(0.5)
    while True:
        answer = input().strip().lower()
        if answer in ["j", "y", "n"]:
            return {"j": True, "y": True, "n": False}[answer]


def get_default_cache():
    return os.path.join(appdirs.user_cache_dir(), "cake")


def exists_default_cache():
    cache_data_path = get_default_cache()
    return os.path.exists(cache_data_path)


def create_default_cache():
    cache_data_path = get_default_cache()
    os.makedirs(cache_data_path, exist_ok=True)
    return cache_data_path


def clean_cache(data_provider):
    """Cleans the cached data in memory and on disk.

    Parameters
    ----------
    data_provider : object
        An object of type `data_provider` (see `datenbaecker`).
    """
    cache = data_provider.cache
    if isinstance(cache, FileCache):
        cache_dir = cache.cache_directory()
        del_cache = ask_delete_cache(cache_dir)
        if del_cache:
            cache.clean_cache()
    else:
        cache.clean_cache()

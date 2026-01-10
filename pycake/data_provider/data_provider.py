import os
import requests
from .theme import print_logo
from .cache import FileCache, InMemoryCache, exists_default_cache, get_default_cache, create_default_cache, ask_cache_data


class LocalDataProvider:
    """
    A class to manage a local data provider.

    Attributes
    ----------
    cache_dir: str
        The directory path for caching data
    """

    def __init__(self, cache_dir):
        """
        Parameters
        ----------
        cache_dir: str
            The directory path for caching data
        """
        self.cache = self._get_file_cache(cache_dir)

    def _get_file_cache(self, cache_dir):
        """Creates a file cache with the provided directory.

        Parameters
        ----------
        cache_dir: str
            The directory path for caching data
        """
        return FileCache(cache_dir)


class RemoteDataProvider:
    """
    A class to manage a remote data provider.

    Attributes
    ----------
    host : str
        The base URL for the remote data provider
    cache_dir : str or None, optional
        The directory path for caching data, or `None` if caching is not used
    auth_info : object or None, optional
        Authentication information for the remote server (currently unused)
    api_version_prefix : str, optional
         The API version prefix for the URL, default is an empty string
    """

    def __init__(self, host, cache_dir=None, auth_info=None, api_version_prefix=""):
        """
        Parameters
        ----------
        host : str
            The base URL for the remote data provider
        cache_dir : str or None, optional
            The directory path for caching data, or `None` if caching is not used
        auth_info : object or None, optional
            Authentication information for the remote server (currently unused)
        api_version_prefix : str, optional
             The API version prefix for the URL, default is an empty string
        """
        self.host = host
        self.auth_info = auth_info
        self.api_version_prefix = api_version_prefix
        self.cache = self._create_cache(cache_dir)

    def _create_cache(self, cache_dir):
        """
        Create a cache instance based on the provided cache directory.

        Parameters
        ----------
        cache_dir : str or bool or None
            - If `str`, use the provided path to create a FileCache.
            - If `True`, a default cache directory will be created.
            - If `False`, InMemoryCache will be used.
            - If `None`, check for existing default cache or prompt to create one.

        Returns
        -------
        FileCache or InMemoryCache
            An instance of FileCache if a valid path is determined,
            otherwise an InMemoryCache.
        """
        if cache_dir is None:
            if exists_default_cache():
                cache_dir = get_default_cache()
            elif ask_cache_data():
                cache_dir = create_default_cache()
        elif isinstance(cache_dir, bool) and cache_dir:
            cache_dir = create_default_cache()

        if isinstance(cache_dir, str):
            return FileCache(cache_dir)
        else:
            return InMemoryCache()


class Datenbaecker(RemoteDataProvider):
    """
    A class to manage the Datenbaecker data provider.

    This class inherits from RemoteDataProvider and is specifically
    designed to interact with the Datenbaecker API.
    """

    def __init__(self, cache_dir=None, auth_info=None):
        baecker_url = os.getenv("CAKE_URL", "https://datacake.datenbaecker.ch/api")
        super().__init__(
            host=baecker_url,
            cache_dir=cache_dir,
            auth_info=auth_info,
            api_version_prefix="v1/"
        )
        self._get_logo()
        self._get_news()

    def _get_logo(self):
        """ Prints the Datenbaecker logo."""
        if connection_counter() == 1:
            print_logo()

    def _get_news(self):
        """
        Connects to the Datenbaecker news endpoint and prints the news content.
        """

        url = os.path.join(self.host, self.api_version_prefix + "news")
        res = requests.get(url)
        res.raise_for_status()
        news = res.json()
        if news != [""]:
            print(f"\n{news}")


def create_default_data_provider():

    default_provider = None

    def get_or_set_default(dp=None):
        nonlocal default_provider
        if dp is not None:
            default_provider = dp
        elif default_provider is None:
            default_provider = Datenbaecker()
        return default_provider

    return get_or_set_default


default_data_provider = create_default_data_provider()


def create_counter(init=0):
    val = init

    def counter(inc=1):
        nonlocal val
        val += inc
        return val
    return counter


connection_counter = create_counter()

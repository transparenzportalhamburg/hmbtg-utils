
import socket
import ssl
import requests
import os
import urllib.request

import cgi
import posixpath

# TYPING
from typing import Tuple
from http.client import HTTPMessage

try:
    from requests.packages.urllib3.exceptions import InsecureRequestWarning
    requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
except Exception:
    pass


class URL:
    """  A Utility Class for URL-handling.
    """
    SPECIAL_CHARS_MAP = {
        '\\u00a7': '%C2%A7',
        '\xa7': '%C2%A7'
    }
    INIT_DEFAULT_TIMEOUT: float = 30.

    def __init__(self, url: str, default_timeout: float = INIT_DEFAULT_TIMEOUT) -> None:
        """

        Args:
            url (str): is an URL String.
        """
        self._url: str = url

        self._default_timeout: float = default_timeout
        self._current_timeout: float = self._default_timeout
        self.reset_timeout()

        ssl._create_default_https_context = ssl._create_unverified_context # Could be deprecated

    def set_timeout(self, timeout: float):
        """Sets the default Timeout for sockets and requests.

        Args:
            timeout (float): default timeout in milliseconds.
        """
        self._current_timeout = timeout
        socket.setdefaulttimeout(self._current_timeout)
    
    def set_default_timeout(self, timeout):
        self._default_timeout = timeout

    def reset_timeout(self):
        """Resets the Timeout to the current default_timeout.
        """
        self.set_timeout(self._default_timeout)
    
    def reset_default_timeout(self):
        """Resets the default_timeout to the initial default_timeout.
        """
        self.set_default_timeout(URL.INIT_DEFAULT_TIMEOUT)

    def to_file(self, target=None) -> Tuple[str, HTTPMessage]:
        """Saves request response to given file target.

        Args:
            target (_type_, optional): filename to  . Defaults to None.

        Returns:
            _type_: 
        """
        return urllib.request.urlretrieve(self._url, target)

    def _default_get(self, timeout):
        timeout = self.get_default_timeout(timeout)
        
        return requests.get(self._url, 
                            allow_redirects=True, 
                            timeout=timeout, 
                            verify=False)
    
    
    def _default_url_open(self, timeout):
        timeout = self.get_default_timeout(timeout)
        context = self.get_default_context()
        
        return urllib.request.urlopen(self._url, context=context, timeout=timeout)

    def get_default_timeout(self, timeout):
        """_summary_

        Args:
            timeout (_type_): _description_

        Returns:
            _type_: _description_
        """
        if timeout is None:
            return self.timeout
        return timeout

    def get_default_context(self):
        """Creates a Default SLL-Context for urllib requests.

        Returns:
            SSLContext: is the returned context.
        """
        context = ssl.create_default_context()
        context.check_hostname = False
        context.verify_mode = ssl.CERT_NONE
        
        return context

    def download(self, filename, timeout=None):
        """Downloads the reponse of this URL.

        Args:
            filename (_type_): is the name of the File.
            timeout (_type_, optional): is a alternative timeout if set None it uses the default timeout. Defaults to None.
        """
        with open(filename, 'wb') as f:
            f.write(self._default_url_open(timeout).read())

    def to_stream(self, timeout=None):
        """Returns a stream of an URL open.
        Args:
            timeout (_type_, optional): overrides the current timeout setting. If its None uses default. Defaults to None.

        Raises:
            Exception: Need to be fixed. Currently throws a gerneral Exception if something went wrong with the URL open.

        Returns:
            _UrlopenRet: url response stream.
        """
        try:
            return self._default_url_open(timeout)
        except Exception:
            #TODO: Fix Exception.
            raise Exception(f'urllib2.urlopen failed for URL {self._url}')
        

    def get_size(self, timeout:float=None) -> int:
        """Returns the size of the retrieved Reponse

        Args:
            timeout (_type_, optional): overrides the current timeout setting. If its None uses default. Defaults to None.

        Returns:
            int: size in bytes.
        """
        
        #TODO: verify, normalize_url 
        result = 0
        try:
            if os.path.isfile(self._url):
                result = os.path.getsize(self._url)
            else:
                response = requests.head(self._url, 
                                         allow_redirects=True, 
                                         timeout=timeout, 
                                         verify=False)
                result = int(response.headers.get('content-length', 0))
                if result == 0:
                    result = len(self.__default_get(timeout).content)
        except Exception:
            pass
        
        return result

    # TODO: change to Str or Byte.
    def get_content(self, encoding: str = 'utf8', timeout=None):
        """Returns content of the URL response.

        Args:
            encoding (str, optional): the encoding used by the source. Defaults to 'utf8'.
            timeout (_type_, optional): overrides the current timeout setting. If its None uses default. Defaults to None.

        Returns:
            bytes: the conntent as bytes.
        """
        res = self._default_get(timeout)
        if encoding:
            return res.content.decode(encoding)
        return res.content

    def get_json(self, headers=None):
        """Returns the reponse of the response as json.

        Args:
            headers (_type_, optional): in case the header needs to change. Defaults to None.

        Returns:
            json: the request reponse.
        """
        return requests.get(self._url, headers=headers, verify=False).json()

    def exists(self):
        """DEPRECATED: PLEASE USE is_reachable().
        Checks if the URL exists or is reachable.

        Returns:
            bool: is reachable
        """
        return self.is_reachable()
        
    def is_reachable(self):
        """Checks if the URL is reachable.

        Returns:
            bool: ture if it is else False."""
        try:
            with requests.get(self._url, stream=True) as response:
                try:
                    response.raise_for_status()
                    return True
                except requests.exceptions.HTTPError:
                    return False
        except requests.exceptions.ConnectionError:
            return False
        

    def is_normalized(self):
        """Cheacks if the URL has special characters.
        Returns:
            bool: true if it is normalized else false.
        """
        for c in self.SPECIAL_CHARS_MAP:
            if c in self._url:
                return False
        return True

    def normalized(self):
        """Normalizes the URL.

        Returns:
            str: normelized URL
        """
        if type(self._url) == str:
            # only treat certain special characters
            # res['url'] = urllib.quote(res['url'], safe=":/")
            for old, new in self.SPECIAL_CHARS_MAP.items():
                url = self._url.replace(old, new)
        return url

    def get_name_of_resource_file(self, timeout=10.):
        """ Returns the Filename of a file based on the url of the file.

        Args:
            timeout (_type_, optional): overrides the current timeout setting. If its None uses default. Defaults to 10..


        Returns:
            str: the name.
        """
        try:
            response = urllib.request.urlopen(self._url, timeout=timeout)
            disposition = response.headers.get('Content-Disposition', '')
            _ , params = cgi.parse_header(disposition)
            filename = params.get('filename')
            
        except Exception:
            filename = None
        # if no filename in header, use part of url
        if not filename:
            path = urllib.parse.urlsplit(self._url).path
            filename = posixpath.basename(path)
        # cut off file extension
        
        return filename.split('.')[0] #TODO: Exception possible. Fix Try Catch.

    def __str__(self):
        return self._url

def normalize_url(url):
    """DEPRECATED!: Please use normalized()

    Args:
        url (_type_): _description_

    Returns:
        _type_: _description_
    """
    return URL(url).normalized()

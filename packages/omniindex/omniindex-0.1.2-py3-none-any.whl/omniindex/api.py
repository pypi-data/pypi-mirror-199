import requests
import json

from omniindex.internal.requester import (
    DEFAULT_TIMEOUT,
    delete_request,
    get_request,
    post_request,
)
from omniindex.internal.utils import urljoin
# Constants


# Classes



class Client:
    """
    Python OmniIndex API client.
    All of the endpoints documented under the ``omniindex.api``
    module may be called from a ``omniindex.Client`` instance.
    """
    def __init__(
        self,
        server=None,
        api_key=None,
        unit_name=None,
        api_version="v1",
        type=None,
        user=None,
        
        **kwargs,
    ):
        """
        Initialize a client with credentials.
        :param  str     server:         Your Omniindex blockchain node server
        :param  str     api_key:        Your password / api key for Omniindex
        :param  str     unit_name:      Organisational unit name
        :param  str     type:           Type of block to be returned
        :param  str     user:           User name
        """        
        self.server = server
        self.api_key = api_key
        self.unit_name = unit_name
        self.api_version = api_version
        self.type = type
        self.user = user
        self.base_url = f"https://api.omniindex.xyz/api_{self.api_version}"
        self.session = requests.Session()
        self.headers = {'Content-Type': 'application/json',
        'Accept': 'application/json'
    }

    
# Functions
def post(
    self, path, payload=None, is_json=True, headers={}, api_version=None
):
    """Make a post request."""
    return self._post(
        path, payload, is_json, self.session, headers, api_version
    )

def _post(
        self, path, payload, is_json, session=None, headers={}, api_version=None
    ):
        headers = {
            **self.headers,
            **headers,
        }
        return post_request(
            urljoin(
                self.base_url,
                f"{self.api_version if not api_version else api_version}{path}",
            ),
            payload=json.dumps({
                "unitName": self.unit_name,
                "server": self.server,
                "Type": self.type,
                "user": self.user,
                "password": self.api_key
            }),
            timeout=self.timeout,
            is_json=is_json,
            headers=headers,
            session=session,
        )



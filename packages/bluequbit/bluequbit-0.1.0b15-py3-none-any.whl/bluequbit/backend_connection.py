import json
import logging
from pathlib import Path

import requests
import requests_toolbelt
import urllib3

from .exceptions import BQAPIError, BQError, BQUnauthorizedAccessError
from .http_adapter import TimeoutHTTPAdapter
from .version import __version__

logger = logging.getLogger("bluequbit-python-sdk")


class BackendConnection:
    def __init__(self, api_token=None, update_config_file=True):
        config_dir = Path.home() / ".config" / "bluequbit"
        config_location = config_dir / "config.json"

        main_endpoint_from_config_file = None
        token_from_config_file = None
        ssl_verify_from_config_file = None

        if config_location.is_file():
            with config_location.open(encoding="utf-8") as f:
                config = json.load(f)
            main_endpoint_from_config_file = config.get("main_endpoint")
            token_from_config_file = config.get("token")
            ssl_verify_from_config_file = config.get("ssl_verify")

        if api_token is None:
            if token_from_config_file is None:
                raise BQError(
                    (
                        "Please specify an API key to init() (or have config written"
                        f" in {config_location}).You can find your API key once you log"
                        " in to https://app.bluequbit.io"
                    ),
                )
            api_token = token_from_config_file

        self._api_config = {
            "token": api_token,
            "main_endpoint": (
                "https://app.bluequbit.io/api/v1"
                if main_endpoint_from_config_file is None
                else main_endpoint_from_config_file
            ),
            "ssl_verify": (
                True
                if ssl_verify_from_config_file is None
                else ssl_verify_from_config_file
            ),
        }

        if (
            api_token is not None
            and api_token != token_from_config_file
            and update_config_file
        ):
            config_dir.mkdir(exist_ok=True, parents=True)
            self.update_config_file(self._api_config, config_location)

        try:
            self._token = self._api_config["token"]
        except KeyError:
            raise BQError(
                (
                    "Incorrect config file: 'token' key is not present in the config"
                    f" file {config_location}."
                ),
            ) from None

        try:
            self._default_headers = {"Authorization": f"SDK {self._token}"}
            self._default_headers["User-Agent"] = requests_toolbelt.user_agent(
                "bluequbit", __version__
            )

            self._main_endpoint = "https://app.bluequbit.io/api/v1"
            if "main_endpoint" in self._api_config:
                self._main_endpoint = self._api_config["main_endpoint"]
            self._verify = True
            if "ssl_verify" in self._api_config:
                self._verify = self._api_config["ssl_verify"]
            self._session = None
            self._authenticated = True
            response = self.send_request(
                req_type="GET",
                path="/jobs",
                params={"limit": 1},
            )
            if not self._verify:
                urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

            if not response.ok:
                self._authenticated = False
                self._session = None
                if response.status_code == 401:
                    raise BQUnauthorizedAccessError
                raise BQAPIError(
                    response.status_code, f"Couldn't reach BlueQubit {response.text}."
                )
        except:
            self._authenticated = False
            self._session = None
            raise

    @staticmethod
    def update_config_file(content, config_location):
        with config_location.open("w", encoding="utf-8") as f:
            json.dump(content, f, indent=4)
        logger.info("Configuration file %s successfully updated.", config_location)

    def send_request(self, req_type, path, params=None, json_req=None):
        if not self._authenticated:
            raise BQError(
                (
                    "BQClient was not initialized. Please provide correct API token to"
                    " BQClient(<token>)."
                ),
            )
        url = self._main_endpoint + path

        if params is not None:
            for key, value in params.items():
                if isinstance(value, str):
                    params[key] = value.replace("\\", "\\\\")

        req = requests.Request(method=req_type, url=url, json=json_req, params=params)
        if self._session is None:
            self._session = self._create_session()
        prepared = self._session.prepare_request(req)
        resp = self._session.send(request=prepared, verify=self._verify)
        return resp

    def _create_session(self):
        session = requests.Session()
        adapter = TimeoutHTTPAdapter()
        session.mount("https://", adapter)
        session.mount("http://", adapter)
        session.headers = self._default_headers

        return session

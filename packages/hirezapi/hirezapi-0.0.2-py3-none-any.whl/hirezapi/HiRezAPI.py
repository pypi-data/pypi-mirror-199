import datetime
import hashlib
import json
import logging

import requests

from hirezapi.enums import ResponseFormat

LOGGER = logging.getLogger(__name__)


class HiRezAPI():
    """_summary_

    Raises:
        Exception: _description_

    Returns:
        _type_: _description_
    """
    endpoint = ""

    def __init__(
            self,
            dev_id,
            auth_key,
            response_format=ResponseFormat.JSON,
            auto_recreate_session=False,
            session_file=None):
        """_summary_

        Args:
            dev_id (_type_): _description_
            auth_key (_type_): _description_
            response_format (_type_, optional): _description_. Defaults to ResponseFormat.JSON.
        """
        self.dev_id = dev_id
        self.auth_key = auth_key
        self._response_format = response_format
        self.auto_create_session = auto_recreate_session
        self.session_file = session_file
        if self.session_file is not None:
            self._load_session()
        else:
            self.session = self._create_session()

    def _create_signature(self, method_name, timestamp):
        """_summary_

        Args:
            method_name (_type_): _description_
            timestamp (_type_): _description_

        Returns:
            _type_: _description_
        """
        signature = self.dev_id + method_name + self.auth_key + timestamp
        return hashlib.md5(signature.encode()).hexdigest()

    def _load_session(self):
        LOGGER.info("Loading session from %s", self.session_file)
        try:
            with open(self.session_file) as session_file:
                session = session_file.read()
                self.session = json.loads(session)
            LOGGER.info("Sucessfully loaded session: %s", self.session["session_id"])
        except FileNotFoundError:
            LOGGER.info("Could not find the session file: %s.  Creating new session.", self.session_file)
            self.session = self._create_session()

    def _save_session(self):
        pass

    def _create_request_url(self, method_name, params=[]):
        """_summary_

        Args:
            method_name (_type_): _description_
            params (list, optional): _description_. Defaults to [].

        Returns:
            _type_: _description_
        """
        timestamp = datetime.datetime.utcnow().strftime("%Y%m%d%H%M%S")
        signature = self._create_signature(method_name, timestamp)
        url = [
            self.endpoint,
            method_name + self._response_format,
            self.dev_id,
            signature,
            self.session["session_id"],
            timestamp
        ] + params
        return "/".join(url)

    def _make_request(self, url):
        """_summary_

        Args:
            url (_type_): _description_

        Raises:
            Exception: _description_

        Returns:
            _type_: _description_
        """
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Failed to fetch data from API. Response code: {response.status_code}")

    def _create_session(self):
        """_summary_

        Returns:
            _type_: _description_
        """
        method_name = "createsession"
        timestamp = datetime.datetime.utcnow().strftime("%Y%m%d%H%M%S")
        url = [
            self.endpoint,
            method_name + self._response_format,
            self.dev_id,
            self._create_signature(method_name, timestamp),
            timestamp
        ]
        return self._make_request(
            "/".join(url)
        )

    def ping(self):
        """_summary_

        Returns:
            _type_: _description_
        """
        return self._make_request(self.endpoint + "/" + "ping" + self._response_format)

    def test_session(self):
        url = self._create_request_url("testsession")
        return self._make_request(url)

    def get_data_used(self):
        url = self._create_request_url("getdataused")
        return self._make_request(url)

    def get_hirez_server_status(self):
        url = self._create_request_url("gethirezserverstatus")
        return self._make_request(url)

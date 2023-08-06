from hirezapi.enums import Endpoints
from hirezapi.enums import ResponseFormat

from .HiRezAPI import HiRezAPI


class SmiteAPI(HiRezAPI):

    def __init__(self, dev_id, auth_id, response_format=ResponseFormat.JSON):
        self.endpoint = Endpoints.SMITE
        super().__init__(dev_id, auth_id, response_format=response_format)

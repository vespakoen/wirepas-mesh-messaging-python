"""
    Process scratchpad
    ===================

    .. Copyright:
        Copyright 2019 Wirepas Ltd under Apache License, Version 2.0.
        See file LICENSE for full license details.
"""

from .proto import GenericMessage

from .request import Request
from .response import Response
from .wirepas_exceptions import GatewayAPIParsingException


class ProcessScratchpadRequest(Request):
    """
    ProcessScratchpadRequest: request to process scratchpad on a given sink

    Attributes:
        sink_id (str): id of the sink (dependant on gateway)
        req_id (int): unique request id
    """

    def __init__(self, sink_id, req_id=None, **kwargs):
        super(ProcessScratchpadRequest, self).__init__(sink_id, req_id, **kwargs)

    @classmethod
    def from_payload(cls, payload):
        message = GenericMessage()
        try:
            message.ParseFromString(payload)
        except Exception:
            # Any Exception is promoted to Generic API exception
            raise GatewayAPIParsingException(
                "Cannot parse ProcessScratchpadRequest payload"
            )

        req = message.wirepas.process_scratchpad_req

        d = Request._parse_request_header(req.header)

        return cls(d["sink_id"], d["req_id"], time_ms_epoch=d["time_ms_epoch"])

    @property
    def payload(self):
        message = GenericMessage()
        # Fill the request header
        req = message.wirepas.process_scratchpad_req
        self._load_request_header(req)

        return message.SerializeToString()


class ProcessScratchpadResponse(Response):
    """
    ProcessScratchpadResponse: Response to answer a ProcessScratchpadRequest

    Attributes:
        req_id (int): unique request id that this Response is associated
        gw_id (str): gw_id (str): gateway unique identifier
        res (GatewayResultCode): result of the operation
        sink_id (str): id of the sink (dependant on gateway)
    """

    def __init__(self, req_id, gw_id, res, sink_id, **kwargs):
        super(ProcessScratchpadResponse, self).__init__(
            req_id, gw_id, res, sink_id, **kwargs
        )

    @classmethod
    def from_payload(cls, payload):
        message = GenericMessage()
        try:
            message.ParseFromString(payload)
        except Exception:
            # Any Exception is promoted to Generic API exception
            raise GatewayAPIParsingException(
                "Cannot parse ProcessScratchpadResponse payload"
            )

        response = message.wirepas.process_scratchpad_resp

        d = Response._parse_response_header(response.header)

        return cls(d["req_id"], d["gw_id"], d["res"], d["sink_id"], time_ms_epoch=d["time_ms_epoch"])

    @property
    def payload(self):
        message = GenericMessage()

        response = message.wirepas.process_scratchpad_resp
        self._load_response_header(response)

        return message.SerializeToString()

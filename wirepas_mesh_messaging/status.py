"""
    Status
    ======

    .. Copyright:
        Copyright 2019 Wirepas Ltd under Apache License, Version 2.0.
        See file LICENSE for full license details.
"""

import enum
from .proto import GenericMessage, ON, OFF

from .event import Event
from .wirepas_exceptions import GatewayAPIParsingException

# This API should never be changes in future (prupose of protobuf)
API_VERSION = 1


class GatewayState(enum.Enum):
    """
    GatewayState

    Enum providing the possible
    states for the gateway

    ONLINE or OFFLINE

    """

    ONLINE = 0
    OFFLINE = 1


class StatusEvent(Event):
    """
    StatusEvent: Event generated by the gateway to set its status (ONLINE/OFFLINE)

    Attributes:
        gw_id (str): gateway unique identifier
        state (GatewayState): state of the gateway
        version (int): API version for gateway. Should be always 1
        event_id(int): event unique id (random value generated if None)
    """

    def __init__(self, gw_id, state, version=API_VERSION, event_id=None, **kwargs):
        super(StatusEvent, self).__init__(gw_id, event_id=event_id, **kwargs)
        self.state = state
        self.version = version

    @classmethod
    def from_payload(cls, payload):
        """ Converts a protobuff message into a python object """
        message = GenericMessage()
        try:
            message.ParseFromString(payload)
        except Exception:
            # Any Exception is promoted to Generic API exception
            raise GatewayAPIParsingException("Cannot parse StatusEvent payload")

        event = message.wirepas.status_event

        if event.state == ON:
            online = GatewayState.ONLINE
        else:
            online = GatewayState.OFFLINE

        if event.version != API_VERSION:
            raise RuntimeError("Wrong API version")

        d = Event._parse_event_header(event.header)
        return cls(d["gw_id"], online, event_id=d["event_id"], time_ms_epoch=d["time_ms_epoch"])

    @property
    def payload(self):
        """ Returns a proto serialization of itself """

        message = GenericMessage()
        # Fill the request header
        status = message.wirepas.status_event
        self._load_event_header(status)

        status.version = API_VERSION
        if self.state == GatewayState.ONLINE:
            status.state = ON
        else:
            status.state = OFF

        return message.SerializeToString()

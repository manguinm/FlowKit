from enum import Enum
from json import loads


__all__ = [
    "ZMQReplyStatus",
    "ZMQReplyMessage",
    "ZMQReplyPayload",
    "ZMQReply",
    "parse_zmq_message",
    "FlowKitZMQError",
]


class ZMQReply:
    """
    Class representing a zmq reply.

    It has the following responsibilities:

      - Ensure that the reply status can only be one of the valid values defined in ZMQReplyStatus.
      - Ensure the JSON structure of the reply (as returned by the as_json() method) is consistent.
    """

    def __init__(self, status, msg="", payload=None):
        """
        Parameters
        ----------
        status : str or
        """
        if msg == "" and payload is None:
            raise ValueError(
                "At least one of the arguments 'msg', 'payload' must be provided."
            )

        self.status = ZMQReplyStatus(status)
        self.msg = ZMQReplyMessage(msg)
        self.payload = ZMQReplyPayload(payload)

    def to_json(self):
        """
        Return a JSON object
        """
        return {"status": self.status.value, "msg": self.msg, "payload": self.payload}

    @classmethod
    def from_json(cls, json_data):
        """
        Deserialise json_data and return a ZMQReply object.
        """
        try:
            key = "status"
            status = json_data[key]

            key = "msg"
            msg = json_data[key]

            key = "payload"
            payload = json_data[key]
        except KeyError:
            # TODO: We should perhaps raise a custom exception here...
            raise ValueError(
                f"JSON data does not represent a valid ZMQReply. Missing key: '{key}'"
            )

        return cls(status=status, msg=msg, payload=payload)


# class ZMQReplyError(Exception):
#     """
#     Exception which indicates an error related to ZMQReply,
#     for example during (de)serialisation to/from JSON.
#     """


class ZMQReplyStatus(str, Enum):
    """
    Valid status values for a zmq reply.
    """

    SUCCESS = "success"
    ERROR = "error"


class ZMQReplyMessage(str):
    """
    Class representing a zmq reply message. The input
    is automatically converted to a string if needed.
    """


class ZMQReplyPayload(dict):
    """
    Class representing payload included in a zmq reply.
    The input is automatically converted to a dict.
    """

    def __init__(self, payload):
        if payload is None:
            payload = {}

        super().__init__(payload)


class FlowKitZMQError(Exception):
    pass


def parse_zmq_message(msg_str):
    """
    Parse the message string and return

    Parameters
    ----------
    msg_str : str
        The message string as received from zmq. This must represent a valid
        JSON object containing the keys `action`, `params`, `request_id`.
        The values of `action` and `request_id` must be strings, while the
        value of `params` must be a dictionary. The `params` key may be omitted
        if the action handler does not expect any arguments.

        Example: {"action": "ping", params={}, "request_id": "<some_request_id>"}

    Returns
    -------
    (str, str, dict)
        Returns a tuple of values containing: the name of the action to be performed;
        the request_id of the request that initiated the action; and a dict with action
        parameters (which can be passed to the action handler).
    """
    # Load JSON from zmq message string.
    try:
        msg = loads(msg_str)
    except ValueError:
        raise FlowKitZMQError("Zmq message did not contain valid JSON.")

    # Ensure there are no unexpected keys present
    msg_keys = list(sorted(msg.keys()))
    if not set(msg_keys).issubset(["action", "params", "request_id"]):
        unexpected_keys = list(
            sorted(set(msg_keys).difference(["action", "params", "request_id"]))
        )
        raise FlowKitZMQError(f"Message contains unexpected key(s): {unexpected_keys}")

    # Determine the action to be performed.
    try:
        action = msg["action"]
    except KeyError:
        raise FlowKitZMQError("Message does not contain expected key: 'action'.")
    if not isinstance(action, str):
        raise FlowKitZMQError("Action must be a string.")

    # Ensure request_id is present.
    try:
        request_id = msg["request_id"]
    except KeyError:
        raise FlowKitZMQError("Message does not contain expected key: 'request_id'.")
    if not isinstance(request_id, str):
        raise FlowKitZMQError("Request id must be a string.")

    # Extract any params to be passed to the action handler.
    try:
        action_params = msg["params"]
    except KeyError:
        action_params = {}
    if not isinstance(action_params, dict):
        raise FlowKitZMQError("Action params must be a dictionary.")

    return action, request_id, action_params

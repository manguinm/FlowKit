from enum import Enum

__all__ = ["ZMQReplyStatus", "ZMQReplyMessage", "ZMQReplyPayload", "ZMQReply"]


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

    ACCEPTED = "accepted"
    DONE = "done"
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

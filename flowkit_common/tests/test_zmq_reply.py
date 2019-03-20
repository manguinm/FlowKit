import pytest
from flowkit_common.zmq_reply import (
    ZMQReply,
    ZMQReplyStatus,
    ZMQReplyMessage,
    ZMQReplyPayload,
)

# Tests for ZMQReply


def test_can_construct_valid_zmq_reply():
    """
    Test that we can construct a ZMQReply and it contains the expected fields.
    """
    reply = ZMQReply(status="accepted", msg="foobar", payload={"a": 1, "b": 2})
    assert "accepted" == reply.status
    assert "foobar" == reply.msg
    assert {"a": 1, "b": 2} == reply.payload


def test_zmq_reply_to_json():
    """
    ZMQReply can be converted to JSON.
    """
    reply = ZMQReply("accepted", msg="foobar", payload={"a": 1, "b": 2})
    expected_json = {"status": "accepted", "msg": "foobar", "payload": {"a": 1, "b": 2}}
    assert expected_json == reply.to_json()


def test_zmq_reply_from_json():
    """
    ZMQReply can be imported from JSON.
    """
    json_data = {"status": "accepted", "msg": "foobar", "payload": {"a": 1, "b": 2}}
    reply = ZMQReply.from_json(json_data)
    assert "accepted" == reply.status
    assert "foobar" == reply.msg
    assert {"a": 1, "b": 2} == reply.payload


def test_at_least_one_of_message_or_payload_must_be_provided():
    """
    At least one of the arguments `msg`, `payload` must be provided.
    """
    with pytest.raises(
        ValueError,
        match="At least one of the arguments 'msg', 'payload' must be provided.",
    ):
        ZMQReply(status="accepted", msg="", payload=None)


def test_missing_key_when_loading_from_json():
    """
    An error is raised if the input JSON data is missing one of the required keys.
    """
    with pytest.raises(
        ValueError,
        match="JSON data does not represent a valid ZMQReply. Missing key: 'status'",
    ):
        ZMQReply.from_json({"msg": "foobar", "payload": {}})

    with pytest.raises(
        ValueError,
        match="JSON data does not represent a valid ZMQReply. Missing key: 'msg'",
    ):
        ZMQReply.from_json({"status": "accepted", "payload": {}})

    with pytest.raises(
        ValueError,
        match="JSON data does not represent a valid ZMQReply. Missing key: 'payload'",
    ):
        ZMQReply.from_json({"status": "accepted", "msg": "foobar"})


#
# Tests for the helper classes ZMQReplyStatus, ZMQReplyMessage, ZMQReplyPayload
#


def test_invalid_reply_status_raises_error():
    """
    Initialising ZMQReplyStatus with an invalid status string raises an error.
    """
    with pytest.raises(ValueError, match="'foobar' is not a valid ZMQReplyStatus"):
        ZMQReplyStatus("foobar")


def test_input_to_ZMQReplyMessage_is_converted_to_a_string():
    """
    Input to ZMQReplyMessage is converted to a string.
    """
    msg = ZMQReplyMessage("foobar")
    assert "foobar" == msg

    msg = ZMQReplyMessage(42)
    assert "42" == msg

    msg = ZMQReplyMessage({"a": 1, "b": 2})
    assert "{'a': 1, 'b': 2}" == msg


def test_input_to_ZMQReplyPayload_is_converted_to_a_dict():
    """
    Input to ZMQReplyPayload is converted to a dict.
    """
    zmq_reply_payload = ZMQReplyPayload({"a": 1})
    assert {"a": 1} == zmq_reply_payload

    # List of tuples is converted to a dict
    zmq_reply_payload = ZMQReplyPayload([("b", 2), ("c", 3)])
    assert {"b": 2, "c": 3} == zmq_reply_payload

    # None is converted to an empty dict
    zmq_reply_payload = ZMQReplyPayload(None)
    assert {} == zmq_reply_payload


def test_zmq_reply_payload_raises_error_for_invalid_input():
    """
    Initialising ZMQReplypayload with invalid input raises an error.
    """
    with pytest.raises(ValueError):
        some_string = "this is not a valid dict"
        ZMQReplyPayload(some_string)

    with pytest.raises(ValueError):
        some_list_of_dicts = [{"a": 1}, {"b": 2}]
        ZMQReplyPayload(some_list_of_dicts)

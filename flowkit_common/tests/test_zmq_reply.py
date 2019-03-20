from flowkit_common import ZMQReply


def test_can_construct_valid_zmq_reply():
    """
    Test that we can construct a ZMQReply and it contains the expected fields.
    """
    reply = ZMQReply(status="accepted", msg="foobar", payload={"a": 1, "b": 2})
    assert "accepted" == reply.status
    assert "foobar" == reply.msg
    assert {"a": 1, "b": 2} == reply.payload

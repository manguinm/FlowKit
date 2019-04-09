import datetime as dt
import pytest

from flowmachine.core.time_slice import (
    TimeSlice,
    FMTimestamp,
    MissingTimestamp,
    FMTimestampError,
)


def test_fm_timestamp():
    ts = FMTimestamp("2016-01-03 11:22:33")
    assert ts == dt.datetime(2016, 1, 3, 11, 22, 33)
    assert ts.as_str() == "2016-01-03 11:22:33"

    ts1 = FMTimestamp("2016-05-09 23:59:31")
    ts2 = FMTimestamp(ts1)
    assert ts1 == dt.datetime(2016, 5, 9, 23, 59, 31)
    assert ts2 == dt.datetime(2016, 5, 9, 23, 59, 31)

    ts = FMTimestamp.from_date("2016-05-12")
    assert ts == dt.datetime(2016, 5, 12, 0, 0, 0)
    assert ts.as_str() == "2016-05-12 00:00:00"

    with pytest.raises(FMTimestampError):
        FMTimestamp("foobar")
    with pytest.raises(FMTimestampError):
        FMTimestamp.from_date("foobar")

    ts1 = FMTimestamp("2016-01-03 11:22:33")
    ts2 = FMTimestamp("2016-08-05 14:58:13")
    assert ts1 == ts1
    assert ts1 != ts2

    ts3 = MissingTimestamp()
    with pytest.raises(
        FMTimestampError, match="MissingTimestamp cannot be converted to a string."
    ):
        ts3.as_str()
    with pytest.raises(
        FMTimestampError, match="MissingTimestamp cannot be converted to a string."
    ):
        str(ts3)
    with pytest.raises(
        FMTimestampError, match="MissingTimestamp does not allow comparison."
    ):
        ts1 == ts3
    with pytest.raises(
        FMTimestampError, match="MissingTimestamp does not allow comparison."
    ):
        ts3 == ts1
    with pytest.raises(
        FMTimestampError, match="MissingTimestamp does not allow comparison."
    ):
        ts3 == ts3
    with pytest.raises(
        FMTimestampError,
        match="Timestamp cannot be compared to object of type <class 'str'>.",
    ):
        ts1 == "foobar"
    with pytest.raises(
        FMTimestampError, match="MissingTimestamp does not allow comparison."
    ):
        ts3 == "foobar"


#
# TODO: the following test contains the behaviour we would *like* to have at the end of this refactoring,
#       but during the refactoring we make it behave like the existing EventTableSubset.
#
# def test_init_with_start_and_end_dates():
#     """
#     Start timestamp is midnight at the beginning of start_date and end timestamp is midnight at the end of `end_date`.
#     """
#     ts = TimeSlice.from_dates(start_date="2016-01-01", end_date="2017-09-23")
#     assert ts.start_timestamp == dt.datetime(2016, 1, 1, 0, 0, 0)
#     assert ts.stop_timestamp == dt.datetime(2017, 9, 24, 0, 0, 0)
#     assert ts.start_timestamp_as_str == "2016-01-01 00:00:00"
#     assert ts.stop_timestamp_as_str == "2017-09-24 00:00:00"


def test_init_with_start_and_end_dates():
    """
    Start timestamp is midnight at the beginning of start_date and end timestamp is midnight at the beginning of `end_date`.
    """
    ts = TimeSlice.from_dates(start_date="2016-01-01", end_date="2017-09-23")
    assert ts.start_timestamp == dt.datetime(2016, 1, 1, 0, 0, 0)
    assert ts.start_timestamp.as_str() == "2016-01-01 00:00:00"
    assert ts.stop_timestamp == dt.datetime(2017, 9, 23, 0, 0, 0)
    assert ts.stop_timestamp.as_str() == "2017-09-23 00:00:00"

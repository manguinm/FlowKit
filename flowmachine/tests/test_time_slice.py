import datetime as dt

from flowmachine.core.time_slice import TimeSlice


#
# TODO: the following test contains the behaviour we would *like* to have at the end of this refactoring,
#       but during the refactoring we make it behave like the existing EventTableSubset.
#
# def test_init_with_start_and_end_dates():
#     """
#     Start timestamp is midnight at the beginning of start_date and end timestamp is midnight at the end of `end_date`.
#     """
#     ts = TimeSlice(start_date="2016-01-01", end_date="2017-09-23")
#     assert ts.start_timestamp == dt.datetime(2016, 1, 1, 0, 0, 0)
#     assert ts.stop_timestamp == dt.datetime(2017, 9, 24, 0, 0, 0)
#     assert ts.start_timestamp_as_str == "2016-01-01 00:00:00"
#     assert ts.stop_timestamp_as_str == "2017-09-24 00:00:00"


def test_init_with_start_and_end_dates():
    """
    Start timestamp is midnight at the beginning of start_date and end timestamp is midnight at the beginning of `end_date`.
    """
    ts = TimeSlice(start_date="2016-01-01", end_date="2017-09-23")
    assert ts.start_timestamp == dt.datetime(2016, 1, 1, 0, 0, 0)
    assert ts.stop_timestamp == dt.datetime(2017, 9, 23, 0, 0, 0)
    assert ts.start_timestamp_as_str == "2016-01-01 00:00:00"
    assert ts.stop_timestamp_as_str == "2017-09-23 00:00:00"

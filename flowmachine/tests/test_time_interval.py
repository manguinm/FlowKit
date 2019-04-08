# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import datetime as dt
import pytest
import textwrap
from sqlalchemy import select

from flowmachine.core.time_interval import TimeInterval
from flowmachine.core.sqlalchemy_table_definitions import EventsCallsTable
from flowmachine.core.sqlalchemy_utils import get_sql_string
from flowmachine.utils import pretty_sql


def test_init_with_strings():
    """
    TimeInterval can be initialised with strings of the form 'YYYY-MM-DD HH:MM:SS'.
    """
    t = TimeInterval(start="2016-03-14 11:22:33", stop="2017-05-12 09:10:52")
    assert t.start == dt.datetime(2016, 3, 14, 11, 22, 33)
    assert t.stop == dt.datetime(2017, 5, 12, 9, 10, 52)
    assert t.start_as_str == "2016-03-14 11:22:33"
    assert t.stop_as_str == "2017-05-12 09:10:52"


def test_malformed_strings():
    """
    TimeInterval raises error if input strings are not in the format 'YYYY-MM-DD HH:MM:SS'.
    """
    with pytest.raises(ValueError):
        TimeInterval(start="Apr 14, 2016 11am", stop="2018-01-01 10:00:00")
    with pytest.raises(ValueError):
        TimeInterval(start="2016-01-01 08:00:00", stop="12/04/2017 08:00:00")

    with pytest.raises(ValueError):
        TimeInterval(start="2016-01-01", stop="2016-02-04 11:22:33")
    with pytest.raises(ValueError):
        TimeInterval(start="2016-01-01 07:00:00", stop="2016-02-04")


def test_start_timestamp_must_not_be_after_stop_timestamp():
    """
    Start timestamp of time interval must not be after stop timestamp.
    """
    with pytest.raises(
        ValueError, match="Start timestamp must not be after stop timestamp."
    ):
        TimeInterval(start="2016-01-05 18:00:00", stop="2016-01-03 09:00:00")


def test_start_timestamp_must_not_be_equal_to_stop_timestamp():
    """
    Start timestamp of time interval must not be equal to stop timestamp.
    """
    with pytest.raises(
        ValueError, match="Start timestamp must not be equal to stop timestamp."
    ):
        TimeInterval(start="2016-01-05 18:00:00", stop="2016-01-05 18:00:00")


def test_must_be_initialised_with_string():
    """
    TimeInterval raises error if initialised with a date/datetime object rather than a string.
    """
    with pytest.raises(
        TypeError,
        match="Initialising TimeInterval with datetime object is not allowed by default.",
    ):
        TimeInterval(start=dt.date(2016, 1, 1), stop="2016-01-03 09:00:00")
    with pytest.raises(
        TypeError,
        match="Initialising TimeInterval with datetime object is not allowed by default.",
    ):
        TimeInterval(start=dt.datetime(2016, 1, 1, 6, 0, 0), stop="2016-01-03 09:00:00")


def test_can_be_initialised_with_date_object_if_explicit_parameter_is_set():
    """
    TimeInterval can be initialised with datetime.date object if `allow_date_objects_during_refactoring=True`.
    """
    t = TimeInterval(
        start=dt.date(2016, 1, 1),
        stop=dt.date(2016, 1, 3),
        allow_date_objects_during_refactoring=True,
    )
    assert t.start_as_str == "2016-01-01 00:00:00"
    assert t.stop_as_str == "2016-01-03 00:00:00"


def test_filter_sqlalchemy_query_by_time_interval():
    """
    TimeInterval can filter a sqlalchemy query to restrict it to the given period.
    """
    time_interval = TimeInterval(
        start="2016-01-03 09:10:44", stop="2017-11-28 18:17:16"
    )

    #
    # Verify the SQL original query
    #
    select_stmt = select([EventsCallsTable.msisdn, EventsCallsTable.datetime])
    sql_expected = pretty_sql(
        textwrap.dedent(
            """
            SELECT events.calls.msisdn, events.calls.datetime
            FROM events.calls
            """
        )
    )
    assert sql_expected == get_sql_string(select_stmt)

    #
    # Verify the SQL of the query filtered by dates
    #
    select_stmt_filtered = time_interval.filter_sqlalchemy_query(
        select_stmt, timestamp_column=EventsCallsTable.datetime
    )
    sql_filtered_expected = pretty_sql(
        textwrap.dedent(
            """
            SELECT events.calls.msisdn,
                   events.calls.datetime
            FROM events.calls
            WHERE events.calls.datetime >= '2016-01-03 09:10:44' AND events.calls.datetime < '2017-11-28 18:17:16'
            """
        )
    )
    assert sql_filtered_expected == get_sql_string(select_stmt_filtered)

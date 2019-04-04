# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import datetime as dt
import pytest
import textwrap
from sqlalchemy import select

from flowmachine.utils import pretty_sql
from flowmachine.core.date_range import DateRange
from flowmachine.core.sqlalchemy_table_definitions import EventsCallsTable
from flowmachine.core.sqlalchemy_utils import get_sql_string


def test_start_and_end_date():
    """
    DateRange knows its start and end date.
    """
    dr = DateRange(start_date="2016-01-01", end_date="2016-01-03")
    assert dr.start_date == dt.date(2016, 1, 1)
    assert dr.end_date == dt.date(2016, 1, 3)
    assert dr.start_date_as_str == "2016-01-01"
    assert dr.end_date_as_str == "2016-01-03"


# def test_start_date_can_be_equal_to_end_date():
#     """
#     Start date can be equal to end date.
#     """
#     dr = DateRange(start_date="2016-01-04", end_date="2016-01-04")
#     assert dr.start_date == dt.date(2016, 1, 4)
#     assert dr.end_date == dt.date(2016, 1, 4)
#     assert dr.start_date_as_str == "2016-01-04"
#     assert dr.end_date_as_str == "2016-01-04"


def test_start_date_must_not_equal_to_end_date():
    """
    Start date must not be equal to end date.
    """
    with pytest.raises(ValueError):
        DateRange(start_date="2016-01-04", end_date="2016-01-04")


def test_start_date_must_not_be_after_end_date():
    """
    Start date of date range must not be after end date.
    """
    with pytest.raises(ValueError, match="Start date must not be after end date."):
        DateRange(start_date="2016-01-05", end_date="2016-01-02")


def test_date_range_accepts_missing_start_date():
    """
    DateRange accepts missing start date
    """
    dr = DateRange(start_date=None, end_date="2016-01-06")
    assert dr.start_date == None
    assert dr.start_date_as_str == None
    assert dr.end_date == dt.date(2016, 1, 6)
    assert dr.end_date_as_str == "2016-01-06"
    assert dr.one_day_past_end_date == dt.date(2016, 1, 7)
    assert dr.one_day_past_end_date_as_str == "2016-01-07"
    with pytest.raises(ValueError, match="Cannot determine length of date range"):
        len(dr)


def test_date_range_accepts_missing_end_date():
    """
    DateRange accepts missing end date
    """
    dr = DateRange(start_date="2016-01-04", end_date=None)
    assert dr.start_date == dt.date(2016, 1, 4)
    assert dr.start_date_as_str == "2016-01-04"
    assert dr.end_date == None
    assert dr.end_date_as_str == None
    assert dr.one_day_past_end_date == None
    assert dr.one_day_past_end_date_as_str == None
    with pytest.raises(ValueError, match="Cannot determine length of date range"):
        len(dr)


def test_date_range_accepts_missing_start_and_end_date():
    """
    DateRange accepts missing start date
    """
    dr = DateRange(start_date=None, end_date=None)
    assert dr.start_date == None
    assert dr.start_date_as_str == None
    assert dr.end_date == None
    assert dr.end_date_as_str == None
    assert dr.one_day_past_end_date == None
    assert dr.one_day_past_end_date_as_str == None
    with pytest.raises(ValueError, match="Cannot determine length of date range"):
        len(dr)


def test_date_range_length():
    """
    Date range knows its length (= number of days it contains).
    """
    # dr = DateRange(start_date="2016-01-03", end_date="2016-01-03")
    # assert len(dr) == 1

    dr = DateRange(start_date="2016-01-04", end_date="2016-01-08")
    assert len(dr) == 5

    dr = DateRange(start_date="2016-01-29", end_date="2016-03-05")
    assert len(dr) == 37


def test_one_day_past_end_date():
    """
    DateRange knows the date after its end date.
    """
    dr = DateRange(start_date="2016-01-07", end_date="2016-01-14")
    assert dr.one_day_past_end_date == dt.date(2016, 1, 15)
    assert dr.one_day_past_end_date_as_str == "2016-01-15"

    dr = DateRange(start_date=dt.date(2016, 4, 12), end_date=dt.date(2016, 5, 31))
    assert dr.one_day_past_end_date == dt.date(2016, 6, 1)
    assert dr.one_day_past_end_date_as_str == "2016-06-01"


@pytest.mark.parametrize(
    "expected_error_type, start_date, end_date",
    [
        (ValueError, "9999-99-99", "2016-01-03"),
        (ValueError, "2016-01-01", "9999-99-99"),
        (TypeError, dt.datetime(2016, 1, 1, 11, 22, 33), "2016-01-03"),
        (TypeError, "2016-01-01", dt.datetime(2016, 1, 1, 11, 22, 33)),
        (TypeError, 42, "2016-01-03"),
        (TypeError, "2016-01-01", 42),
    ],
)
def test_invalid_start_or_end_dates(expected_error_type, start_date, end_date):
    """
    DateRange knows the date after its end date.
    """
    with pytest.raises(expected_error_type):
        DateRange(start_date=start_date, end_date=end_date)


def test_filter_sqlalchemy_query_by_date_range():
    """
    DateRange can filter a sqlalchemy query to restrict it to the given dates.
    """
    date_range = DateRange(start_date="2016-01-01", end_date="2016-01-03")

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
    select_stmt_filtered = date_range.filter_sqlalchemy_query(
        select_stmt, date_column=EventsCallsTable.datetime
    )
    sql_filtered_expected = pretty_sql(
        textwrap.dedent(
            """
            SELECT events.calls.msisdn, events.calls.datetime
            FROM events.calls
            WHERE events.calls.datetime >= '2016-01-01' AND events.calls.datetime < '2016-01-03'
            """
        )
    )
    assert sql_filtered_expected == get_sql_string(select_stmt_filtered)


def test_filter_sqlalchemy_query_by_date_range_with_missing_start_date():
    """
    DateRange can filter a sqlalchemy query by date range with missing start date
    """
    date_range = DateRange(start_date=None, end_date="2016-01-05")

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
    select_stmt_filtered = date_range.filter_sqlalchemy_query(
        select_stmt, date_column=EventsCallsTable.datetime
    )
    sql_filtered_expected = pretty_sql(
        textwrap.dedent(
            """
            SELECT events.calls.msisdn, events.calls.datetime
            FROM events.calls
            WHERE events.calls.datetime < '2016-01-05'
            """
        )
    )
    assert sql_filtered_expected == get_sql_string(select_stmt_filtered)


def test_filter_sqlalchemy_query_by_date_range_with_missing_end_date():
    """
    DateRange can filter a sqlalchemy query by date range with missing end date
    """
    date_range = DateRange(start_date="2016-01-04", end_date=None)

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
    select_stmt_filtered = date_range.filter_sqlalchemy_query(
        select_stmt, date_column=EventsCallsTable.datetime
    )
    sql_filtered_expected = pretty_sql(
        textwrap.dedent(
            """
            SELECT events.calls.msisdn, events.calls.datetime
            FROM events.calls
            WHERE events.calls.datetime >= '2016-01-04'
            """
        )
    )
    assert sql_filtered_expected == get_sql_string(select_stmt_filtered)


def test_filter_sqlalchemy_query_by_date_range_with_missing_start_and_end_date():
    """
    DateRange can filter a sqlalchemy query by date range with missing start and end date
    """
    date_range = DateRange(start_date=None, end_date=None)

    #
    # Verify the SQL original query and check that the filtered one is identical
    # (because there are no constraints on the date range).
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

    select_stmt_filtered = date_range.filter_sqlalchemy_query(
        select_stmt, date_column=EventsCallsTable.datetime
    )
    assert sql_expected == get_sql_string(select_stmt_filtered)

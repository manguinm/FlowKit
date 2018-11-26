# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""
Tests for the spatial activity class
"""
import pytest

from flowmachine.features import TotalLocationEvents


@pytest.mark.parametrize("interval", TotalLocationEvents.allowed_levels)
def test_total_location_events_column_names(exemplar_level_param, get_dataframe):
    """
    TotalLocationEvents() returns data at the level of the cell.
    """

    te = TotalLocationEvents("2016-01-01", "2016-01-04", **exemplar_level_param)
    df = get_dataframe(te)

    assert df.column.tolist() == te.column_names


def test_events_at_cell_level(get_dataframe):
    """
    TotalLocationEvents() returns data at the level of the cell.
    """

    te = TotalLocationEvents("2016-01-01", "2016-01-04", level="versioned-site")
    df = get_dataframe(te)

    # Test one of the values
    df.date = df.date.astype(str)
    val = list(
        df[(df.date == "2016-01-03") & (df.site_id == "zArRjg") & (df.hour == 17)].total
    )[0]
    assert val == 3


def test_ignore_texts(get_dataframe):
    """
    TotalLocationEvents() can get the total activity at cell level excluding texts.
    """
    te = TotalLocationEvents(
        "2016-01-01", "2016-01-04", level="versioned-site", table="events.calls"
    )
    df = get_dataframe(te)

    # Test one of the values
    df.date = df.date.astype(str)
    val = list(
        df[(df.date == "2016-01-01") & (df.site_id == "0xqNDj") & (df.hour == 3)].total
    )[0]
    assert val == 3


def test_only_incoming(get_dataframe):
    """
    TotalLocationEvents() can get activity, ignoring outgoing calls.
    """
    te = TotalLocationEvents(
        "2016-01-01", "2016-01-04", level="versioned-site", direction="in"
    )
    df = get_dataframe(te)
    # Test one of the values
    df.date = df.date.astype(str)
    val = list(
        df[(df.date == "2016-01-01") & (df.site_id == "6qpN0p") & (df.hour == 0)].total
    )[0]
    assert val == 2


def test_events_daily(get_dataframe):
    """
    TotalLocationEvents() can get activity on a daily level.
    """
    te = TotalLocationEvents(
        "2016-01-01", "2016-01-04", level="versioned-site", interval="day"
    )
    df = get_dataframe(te)

    # Test one of the values
    df.date = df.date.astype(str)
    val = list(df[(df.date == "2016-01-03") & (df.site_id == "B8OaG5")].total)[0]
    assert val == 95


def test_events_min(get_dataframe):
    """
    TotalLocationEvents() can get events on a min-by-min basis.
    """
    te = TotalLocationEvents(
        "2016-01-01", "2016-01-04", level="versioned-site", interval="min"
    )
    df = get_dataframe(te)

    # Test one of the values
    df.date = df.date.astype(str)
    val = list(
        df[
            (df.date == "2016-01-03")
            & (df.site_id == "zdNQx2")
            & (df.hour == 15)
            & (df["min"] == 20)
        ].total
    )[0]
    assert val == 1

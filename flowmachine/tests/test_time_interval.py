# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import datetime as dt
import pytest

from flowmachine.core.time_interval import TimeInterval


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


def test_start_timestamp_must_not_equal_stop_timestamp():
    """
    Start timestamp of time interval must not be equal to stop timestamp.
    """
    with pytest.raises(
        ValueError, match="Start timestamp must not be equal to stop timestamp."
    ):
        TimeInterval(start="2016-01-05 18:00:00", stop="2016-01-05 18:00:00")

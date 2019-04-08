# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import datetime as dt

from flowmachine.core.time_interval import TimeInterval


def test_init_with_strings():
    """
    TimeInterval can be initialised with strings of the form 'YYYY-MM-DD HH:MM:SS'.
    """
    dp = TimeInterval(start="2016-03-14 11:22:33", stop="2017-05-12 09:10:52")
    assert dp.start == dt.datetime(2016, 3, 14, 11, 22, 33)
    assert dp.stop == dt.datetime(2017, 5, 12, 9, 10, 52)
    assert dp.start_as_str == "2016-03-14 11:22:33"
    assert dp.stop_as_str == "2017-05-12 09:10:52"

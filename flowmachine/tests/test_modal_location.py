# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import textwrap

from flowmachine.features import daily_location, ModalLocation
from flowmachine.utils import list_of_dates


def test_inferred_start():
    """
    The start datetime is correctly inferred from a list of locations.
    """
    dls = [
        daily_location("2016-01-01", stop="2016-01-02", method="most-common"),
        daily_location("2016-01-02", stop="2016-01-03", method="most-common"),
        daily_location("2016-01-03", stop="2016-01-04", method="most-common"),
    ]
    ml = ModalLocation(*dls)
    assert "2016-01-01 00:00:00" == ml.start


def test_inferred_start_shuffled():
    """
    The start datetime is correctly inferred from a disordered list of locations.
    """
    dls = [
        daily_location("2016-01-03", stop="2016-01-04", method="most-common"),
        daily_location("2016-01-02", stop="2016-01-03", method="most-common"),
        daily_location("2016-01-01", stop="2016-01-02", method="most-common"),
    ]
    ml = ModalLocation(*dls)
    assert "2016-01-01 00:00:00" == ml.start


def test_selected_values(get_dataframe):
    """
    ModalLocation() values are correct.
    """
    mdf = get_dataframe(
        ModalLocation(
            *[daily_location(d) for d in list_of_dates("2016-01-01", "2016-01-03")]
        )
    ).set_index("subscriber")

    expected_result = textwrap.dedent(
        f"""\
        subscriber,pcod
        038OVABN11Ak4W5P,524 4 12 62
        09NrjaNNvDanD8pk,524 5 13 67
        0ayZGYEQrqYlKw6g,524 3 09 51
        0DB8zw67E9mZAPK2,524 4 12 62
        0Gl95NRLjW2aw8pW,524 3 08 44
        0gmvwzMAYbz5We1E,524 4 12 62
        0MQ4RYeKn7lryxGa,524 3 08 44
        0NVaL8k1nwRwOmlg,524 3 08 44
        0W71ObElrz5VkdZw,524 4 12 65
        0Ze1l70j0LNgyY4w,524 2 05 24
        """
    )
    result = mdf.head(10).to_csv()
    assert expected_result == result

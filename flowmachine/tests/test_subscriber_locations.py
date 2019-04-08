# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.


from flowmachine.features.utilities.subscriber_locations import subscriber_locations


def test_can_get_pcods(get_dataframe):
    """
    subscriber_locations() can make queries at the p-code level.
    """

    subscriber_pcod = subscriber_locations(
        "2016-01-01",
        "2016-01-03",
        level="polygon",
        polygon_table="geography.admin3",
        column_name="admin3pcod",
    )
    df = get_dataframe(subscriber_pcod)
    assert df.admin3pcod[0] == "524 3 08 44"

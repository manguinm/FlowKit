# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import datetime as dt


class TimeInterval:
    """
    Represents a time interval between two timestamps. It is
    considered as the half-open interval [start, stop), in
    other words the `stop` timestamp is excluded.
    Timestamps must be specified in the format YYYY-MM-DD HH:MM:SS.
    """

    def __init__(self, start, stop):
        self.start = self._parse_timestamp(start)
        self.stop = self._parse_timestamp(stop)
        self.start_as_str = self.start.strftime("%Y-%m-%d %H:%M:%S")
        self.stop_as_str = self.stop.strftime("%Y-%m-%d %H:%M:%S")

        if self.start > self.stop:
            raise ValueError("Start timestamp must not be after stop timestamp.")
        if self.start == self.stop:
            raise ValueError("Start timestamp must not be equal to stop timestamp.")

    def __repr__(self):
        return f"TimeInterval(start={self.start_as_str}, stop={self.stop_as_str})"

    def _parse_timestamp(self, input_timestamp):
        ts = dt.datetime.strptime(input_timestamp, "%Y-%m-%d %H:%M:%S")
        return ts

    def filter_sqlalchemy_query(self, sqlalchemy_query, *, timestamp_column):
        """
        Parameters
        ----------
        sqlalchemy_query : sqlalchemy.sql.selectable.Select
            The sqlalchemy query to be filtered.
        timestamp_column : sqlalchemy.sql.schema.Column
            The column to filter.

        Returns
        -------
        sqlalchemy.sql.selectable.Select
            The new sqlalchemy query which includes the timestamp filter.
        """
        res = sqlalchemy_query
        res = res.where(timestamp_column >= self.start_as_str)
        res = res.where(timestamp_column < self.stop_as_str)
        return res

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import datetime as dt


class DateRange:
    """
    Represents a time period between a start date and an end date.
    """

    def __init__(self, start_date, end_date):
        self.start_date, self.start_date_as_str = self._parse_date(start_date)
        self.end_date, self.end_date_as_str = self._parse_date(end_date)

        if (
            (self.start_date is not None)
            and (self.end_date is not None)
            and (self.start_date >= self.end_date)
        ):
            raise ValueError(
                "Start date must not be after end date. "
                f"Got: start_date={self.start_date_as_str}, end_date={self.end_date_as_str}"
            )

        if self.end_date is not None:
            self.one_day_past_end_date = self.end_date + dt.timedelta(days=1)
            self.one_day_past_end_date_as_str = self.one_day_past_end_date.strftime(
                "%Y-%m-%d"
            )
        else:
            self.one_day_past_end_date = None
            self.one_day_past_end_date_as_str = None

    def __repr__(self):
        return f"DatePeriod(start_date={self.start_date_as_str}, end_date={self.end_date_as_str})"

    def __len__(self):
        """
        Return number of days contained in this date range.
        """
        if self.start_date is not None and self.end_date is not None:
            return (self.end_date - self.start_date).days + 1
        else:
            raise ValueError(
                "Cannot determine length of date range (start date or end date is undefined)"
            )

    def _parse_date(self, input_date):
        if input_date is None:
            return None, None
        elif isinstance(input_date, dt.date):
            if isinstance(input_date, dt.datetime):
                # Need a bit of gymnastics because dt.date is a subtype of dt.datetime
                raise TypeError(
                    "Date must be an instance of datetime.date, but got datetime.datetime"
                )
            else:
                return input_date, input_date.strftime("%Y-%m-%d")

        elif isinstance(input_date, str):
            try:
                date = dt.datetime.strptime(input_date, "%Y-%m-%d").date()
                return date, date.strftime("%Y-%m-%d")
            except ValueError:
                raise ValueError(
                    f"Date string must represent a valid date in the format 'YYYY-MM-DD'. Got: '{input_date}'"
                )
        else:
            raise TypeError(
                f"Date must be a string of the format YYYY-MM-DD or a datetime.date object. Got: {type(input_date)}"
            )

    def filter_sqlalchemy_query(self, sqlalchemy_query, *, date_column):
        """
        Parameters
        ----------
        sqlalchemy_query : sqlalchemy.sql.selectable.Select
            The sqlalchemy query to be filtered.
        date_column : sqlalchemy.sql.schema.Column
            The column to filter by date.

        Returns
        -------
        sqlalchemy.sql.selectable.Select
            The new sqlalchemy query which includes the date range filter.
        """
        res = sqlalchemy_query
        if self.start_date is not None:
            res = res.where(date_column >= self.start_date_as_str)
        if self.end_date is not None:
            res = res.where(date_column < self.end_date_as_str)
        return res

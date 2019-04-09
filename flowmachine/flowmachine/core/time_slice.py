import datetime as dt


class TimeSlice:
    def __init__(self, *, start_date, end_date):
        """
        Initialise time slice from start and end date.

        The time slice is represented as the half-open time interval [start_timestamp, stop_timestamp),
        where start_timestamp is midnight at the beginning of the the start date and stop_timestamp is
        midnight at the beginning of the day _after_ the end date.

        For example, if start_date="2016-01-01" and end_date="2016-01-07" then the resulting interval
        is `[2016-01-01 00:00:00, 2016-01-08 00:00:00)`.

        Parameters
        ----------
        start_date : str
            ISO format date string for the beginning of the time slice, e.g. "2016-01-01".
        end_date : str
            ISO format date string for the end of the time slice, e.g. "2016-01-07".
        """
        ts_start_date = self._parse_date_as_timestamp(start_date)
        ts_end_date = self._parse_date_as_timestamp(end_date)

        self.start_timestamp = ts_start_date
        self.stop_timestamp = ts_end_date
        # self.stop_timestamp = ts_end_date + dt.timedelta(days=1)
        self.start_timestamp_as_str = self.start_timestamp.strftime("%Y-%m-%d %H:%M:%S")
        self.stop_timestamp_as_str = self.stop_timestamp.strftime("%Y-%m-%d %H:%M:%S")

    def _parse_date_as_timestamp(self, date_str):
        assert isinstance(date_str, str)
        return dt.datetime.strptime(date_str, "%Y-%m-%d")

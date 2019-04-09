import datetime as dt


class TimeSlice:
    def __init__(self, *, start, stop):
        assert isinstance(start, str)
        assert isinstance(stop, str)

        self.start_timestamp = dt.datetime.strptime(start, "%Y-%m-%d %H:%M:%S")
        self.stop_timestamp = dt.datetime.strptime(stop, "%Y-%m-%d %H:%M:%S")
        self.start_timestamp_as_str = self.start_timestamp.strftime("%Y-%m-%d %H:%M:%S")
        self.stop_timestamp_as_str = self.stop_timestamp.strftime("%Y-%m-%d %H:%M:%S")

    @classmethod
    def from_dates(cls, *, start_date, end_date):
        """
        Initialise time slice with a start and end date.

        The time slice is represented as the half-open time interval [start_timestamp, stop_timestamp),
        where start_timestamp is midnight at the beginning of the the start date and stop_timestamp is
        midnight at the beginning of the day _after_ the end date.

        For example, if start_date="2016-01-01" and end_date="2016-01-07" then the resulting interval
        is `[2016-01-01 00:00:00, 2016-01-08 00:00:00)`.

        NOTE: during ongoing refactoring this behaviour is actually different so that the end timestamp
        is actually midnight at the beginning of `end_date`, rather than of the day after `end_date`.

        Parameters
        ----------
        start_date : str
            ISO format date string for the beginning of the time slice, e.g. "2016-01-01".
        end_date : str
            ISO format date string for the end of the time slice, e.g. "2016-01-07".
        """
        ts_start_date = cls._parse_date_as_timestamp(start_date)
        ts_end_date = cls._parse_date_as_timestamp(end_date)

        start_timestamp = ts_start_date
        stop_timestamp = ts_end_date
        # stop_timestamp = ts_end_date + dt.timedelta(days=1)  # TODO: re-enable this after refactoring is done

        # TODO: once TimeSlice supports initialisation directly from timestamps
        # we can remove this and pass start_timestamp/stop_timestamp directly to
        # TimeSlice.__init__()
        start_str = start_timestamp.strftime("%Y-%m-%d %H:%M:%S")
        stop_str = stop_timestamp.strftime("%Y-%m-%d %H:%M:%S")

        return TimeSlice(start=start_str, stop=stop_str)

    @classmethod
    def _parse_date_as_timestamp(cls, date_str):
        assert isinstance(date_str, str)
        return dt.datetime.strptime(date_str, "%Y-%m-%d")

import datetime as dt


class FMTimestampError(Exception):
    pass


class FMTimestamp:
    def __init__(self, ts):
        try:
            self._ts = dt.datetime.strptime(ts, "%Y-%m-%d %H:%M:%S")
        except (TypeError, ValueError):
            raise FMTimestampError(
                f"Timestamp must be a string in the format 'YYYY-MM-DD HH:MM:SS'. Got: '{ts}' (type: {type(ts)})"
            )
        self.is_missing = False

    @classmethod
    def from_date(cls, date_str):
        if date_str is None:
            return MissingTimestamp()
        else:
            try:
                ts = dt.datetime.strptime(date_str, "%Y-%m-%d")
                return cls(ts.strftime("%Y-%m-%d %H:%M:%S"))
            except (TypeError, ValueError):
                raise FMTimestampError(
                    f"Timestamp must be a date string in the format 'YYYY-MM-DD'. Got: {date_str}"
                )

    @classmethod
    def from_any_input(cls, x):
        if isinstance(x, FMTimestamp):
            return x
        else:
            return FMTimestamp(x)

    @classmethod
    def from_legacy_input(cls, x):
        if isinstance(x, FMTimestamp):
            return x
        elif isinstance(x, str):
            try:
                return FMTimestamp.from_date(x)
            except FMTimestampError:
                try:
                    return FMTimestamp(x)
                except FMTimestampError:
                    raise FMTimestampError(f"Could not parse legacy input: {x}")
        else:
            raise FMTimestampError(f"Could not parse legacy input: {x}")

    def __str__(self):
        return self._ts.strftime("%Y-%m-%d %H:%M:%S")

    def as_str(self):
        return str(self)

    def __eq__(self, other):
        if isinstance(other, dt.datetime):
            return self._ts == other
        elif isinstance(other, FMTimestamp):
            return self._ts == other._ts
        else:
            raise FMTimestampError(
                f"Timestamp cannot be compared to object of type {type(other)}."
            )


class MissingTimestamp(FMTimestamp):
    """
    Represents a missing timestamp.
    """

    def __init__(self):
        self.is_missing = True

    def __str__(self):
        raise FMTimestampError("MissingTimestamp cannot be converted to a string.")

    def as_str(self):
        return str(self)

    def __eq__(self, other):
        raise FMTimestampError("MissingTimestamp does not allow comparison.")


class TimeSlice:
    def __init__(self, *, start, stop, parse_legacy_input=False):
        if parse_legacy_input:
            # This is a temporary workaround during refactoring, because a lot of query classes
            # pass in date/datetime objects in various formats.
            self.start_timestamp = FMTimestamp.from_legacy_input(start)
            self.stop_timestamp = FMTimestamp.from_legacy_input(stop)
        else:
            self.start_timestamp = FMTimestamp.from_any_input(start)
            self.stop_timestamp = FMTimestamp.from_any_input(stop)

    def __repr__(self):
        return f"TimeSlice(start={self.start_timestamp.as_str()!r}, stop={self.stop_timestamp.as_str()!r})"

    @classmethod
    def from_legacy_input(cls, *, start, stop):
        return cls(start=start, stop=stop, parse_legacy_input=True)

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
        ts_start_date = FMTimestamp.from_date(start_date)
        ts_end_date = FMTimestamp.from_date(end_date)
        return cls(start=ts_start_date, stop=ts_end_date)

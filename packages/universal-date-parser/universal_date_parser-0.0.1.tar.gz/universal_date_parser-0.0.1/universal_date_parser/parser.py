import re
import locale
import warnings

from datetime import date, time, datetime, timedelta


def date_time_finder(date_in_str) -> (str, str):
    """
    Find the date and time part of the date string.
    """

    date: str
    time: str

    # e.g., 2021-11-19T00:00:34+00:00
    if re.search(r"T\d{2}:\d{2}:\d{2}\+\d{2}:\d{2}", date_in_str) is not None:
        time = re.findall(r"T\d{2}:\d{2}:\d{2}\+\d{2}:\d{2}", date_in_str)[0]
        date = date_in_str.replace(time, "").strip()
        time = time.replace("T", "").replace("+", " ").strip()

    # e.g., 2020-07-16T15:33:30.655Z
    elif re.search(r"T\d{2}:\d{2}:\d{2}\.\d+Z", date_in_str) is not None:
        time = re.findall(r"T\d{2}:\d{2}:\d{2}\.\d+Z", date_in_str)[0]
        date = date_in_str.replace(time, "").strip()
        time = time.replace("T", "").replace("Z", "").split(".")[0].strip()

    # e.g., 2020-07-16T15:33:30Z
    elif re.search(r"T\d{2}:\d{2}:\d{2}Z", date_in_str) is not None:
        time = re.findall(r"T\d{2}:\d{2}:\d{2}Z", date_in_str)[0]
        date = date_in_str.replace(time, "").strip()
        time = time.replace("T", "").replace("Z", " ").strip()

    elif re.search(r"\d{2}:\d{2}:\d{2}", date_in_str) is not None:
        time = re.findall(r"\d{2}:\d{2}:\d{2}", date_in_str)[0]
        date = date_in_str.replace(time, "").strip()

    elif re.search(r"\d:\d{2}:\d{2}", date_in_str) is not None:
        # TODO! normally this is not correct
        time = re.findall(r"\d:\d{2}:\d{2}", date_in_str)[0]
        date = date_in_str.replace(time, "").strip()

    else:
        time = ""
        date = date_in_str

    return date, time


def decl_remover(date_in_str: str) -> str:
    # TODO add some more by checking the local json

    return date_in_str.replace("/", "-").replace(".", "-")


class LetterMonthFinder:
    def __init__(self, date_in_str: str, **kwargs):
        self.date_in_str: str = date_in_str
        self.locale: str = kwargs['locale'] if 'locale' in kwargs else locale.getlocale()[0]

        self.date_format: str

        if re.search(r"\d{4}-", self.date_in_str) is not None or re.search(r"-\d{4}", self.date_in_str) is not None:
            # YYYY
            if re.search(r"\d{4}-[a-zA-Z]{3}-\d{2}", self.date_in_str) is not None:
                # e.g., 2020-Jul-16
                self.date_format = "%Y-%b-%d"
            elif re.search(r"\d{4}-[a-zA-Z]+-\d{2}", self.date_in_str) is not None:
                # e.g., 2020-July-16
                self.date_format = "%Y-%B-%d"
            elif re.search(r"\d{2}-[a-zA-Z]{3}-\d{4}", self.date_in_str) is not None:
                # e.g., 16-Jul-2020
                self.date_format = "%d-%b-%Y"
            elif re.search(r"\d{2}-[a-zA-Z]+-\d{4}", self.date_in_str) is not None:
                # e.g., 16-July-2020
                self.date_format = "%d-%B-%Y"
            elif re.search(r"[a-zA-Z]{3}-\d{2}-\d{4}", self.date_in_str) is not None:
                # e.g., Jul-16-2020
                self.date_format = "%b-%d-%Y"
            elif re.search(r"[a-zA-Z]+-\d{2}-\d{4}", self.date_in_str) is not None:
                # e.g., July-16-2020
                self.date_format = "%B-%d-%Y"
            else:
                raise ValueError(f"Date string '{self.date_in_str}' is not in a valid format")
        else:
            # yy
            if re.search(r"\d{2}-[a-zA-Z]{3}-\d{2}", self.date_in_str) is not None:
                # e.g., 16-Jul-20
                warnings.warn("Date format is ambiguous. dd-b-yy is applied.")
                self.date_format = "%d-%b-%y"
            elif re.search(r"[a-zA-Z]{3}-\d{2}-\d{2}", self.date_in_str) is not None:
                # e.g., Jul-16-20
                self.date_format = "%b-%d-%y"
            elif re.search(r"\d{2}-[a-zA-Z]+-\d{2}", self.date_in_str) is not None:
                # e.g., 16-July-20
                warnings.warn("Date format is ambiguous. dd-B-yy is applied.")
                self.date_format = "%d-%B-%y"
            elif re.search(r"[a-zA-Z]+-\d{2}-\d{2}", self.date_in_str) is not None:
                # e.g., July-16-20
                self.date_format = "%B-%d-%y"
            else:
                raise ValueError(f"Date string '{self.date_in_str}' is not in a valid format")

    def __repr__(self):
        return f"LetterMonthFinder('{self.date_in_str}', locale='{self.locale}')"

    def to_datetime(self) -> date:

        a_datetime: datetime
        if self.locale is not None:
            locale.setlocale(locale.LC_ALL, self.locale)
            a_datetime = datetime.strptime(self.date_in_str, self.date_format)
        else:
            a_datetime = datetime.strptime(self.date_in_str, self.date_format)
        return a_datetime.date()

    def to_str(self, date_format: str = "%Y-%m-%d") -> str:
        return self.to_datetime().strftime(date_format)


class NumberMonthFinder:
    def __init__(self, date_in_str: str, **kwargs):
        self.date_in_str: str = date_in_str
        self.locale: str = kwargs['locale'] if 'locale' in kwargs else locale.getlocale()[0]

        self.date_format: str
        if re.search(r"\d{4}-", self.date_in_str) is not None or re.search(r"-\d{4}", self.date_in_str) is not None:
            # YYYY
            if re.search(r"\d{4}-\d{2}-\d{2}", self.date_in_str) is not None:
                # e.g., 2020-07-16
                self.date_format = "%Y-%m-%d"
            elif re.search(r"\d{2}-\d{2}-\d{4}", self.date_in_str) is not None:
                if self.locale is not None:
                    if self.locale == "en_US":
                        self.date_format = "%m-%d-%Y"
                    else:
                        # by default, dd-mm-YYYY is applied
                        self.date_format = "%d-%m-%Y"
                else:
                    d_m_case: list[bool] = [
                        re.search(r"1[3-9]-\d{2}-\d{4}", self.date_in_str) is not None,  # 13-07-2020
                        re.search(r"2[0-9]-\d{2}-\d{4}", self.date_in_str) is not None,  # 20-07-2020
                        re.search(r"3[0-1]-\d{2}-\d{4}", self.date_in_str) is not None,  # 31-07-2020
                    ]
                    m_d_case: list[bool] = [
                        re.search(r"\d{2}-1[3-9]-\d{4}", self.date_in_str) is not None,  # 07-13-2020
                        re.search(r"\d{2}-2[0-9]-\d{4}", self.date_in_str) is not None,  # 07-20-2020
                        re.search(r"\d{2}-3[0-1]-\d{4}", self.date_in_str) is not None,  # 07-31-2020
                    ]
                    if any(d_m_case):
                        self.date_format = "%d-%m-%Y"
                    elif any(m_d_case):
                        self.date_format = "%m-%d-%Y"
                    else:
                        warnings.warn("Date format is ambiguous. dd-mm-YYYY is applied.")
                        self.date_format = "%d-%m-%Y"
            else:
                raise ValueError(f"Date string '{self.date_in_str}' is not in a valid format")
        else:
            # yy
            if re.search(r"\d{2}-\d{2}-\d{2}", self.date_in_str) is not None:

                if self.locale is not None:
                    if self.locale == "en_US":
                        self.date_format = "%m-%d-%y"
                    else:
                        # by default, dd-mm-YYYY is applied
                        warnings.warn("Date format is ambiguous. dd-mm-yy is applied.")
                        self.date_format = "%d-%m-%y"
                else:
                    d_m_y_case: list[bool] = [
                        re.search(r"3[0-1]-\d{2}-\d{2}", self.date_in_str) is not None,  # 31-07-20
                    ]
                    m_d_y_case: list[bool] = [
                        re.search(r"\d{2}-3[0-1]-\d{2}", self.date_in_str) is not None,  # 07-31-20
                    ]
                    if any(d_m_y_case):
                        self.date_format = "%d-%m-%y"
                    elif any(m_d_y_case):
                        self.date_format = "%m-%d-%y"
                    else:
                        warnings.warn("Date format is ambiguous. yy-mm-dd is applied.")
                        self.date_format = "%y-%m-%d"
            else:
                raise ValueError(f"Date string '{self.date_in_str}' is not in a valid format")

    def __repr__(self):
        return f"NumberMonthFinder('{self.date_in_str}', locale='{self.locale}')"

    def to_datetime(self) -> date:

        a_datetime: datetime = datetime.strptime(self.date_in_str, self.date_format)
        return a_datetime.date()

    def to_str(self, date_format: str = "%Y-%m-%d") -> str:
        return self.to_datetime().strftime(date_format)


class DateParser:

    def __init__(self, date_in_str: str, **kwargs):
        self.date_in_str: str = date_in_str

        # using re to check if there is any number in the date string
        if re.search(r"\d", self.date_in_str) is None:
            raise ValueError(f"Date string '{self.date_in_str}' contains no number")

        self.locale: str = kwargs['locale'] if 'locale' in kwargs else locale.getlocale()[0]

        self.date: datetime
        self.date_format: str = kwargs['date_format'] if 'date_format' in kwargs else "guess"
        if self.date_format != "guess":
            self.date = datetime.strptime(self.date_in_str, self.date_format)
        else:
            if re.search(r'(3|4)\d{4}\.\d+', self.date_in_str):
                # it is probably a date in Excel format
                try:
                    # TODO! use exception to handle unexpected input
                    self.date = datetime.strptime('1899-12-30', '%Y-%m-%d') + timedelta(days=float(self.date_in_str))
                except:
                    pass
            else:
                a_date: str
                a_time: str
                a_date_date: date
                a_time_time: time

                a_date, a_time = date_time_finder(date_in_str)
                a_date = decl_remover(a_date)
                if re.search(r"[a-zA-Z]", a_date) is not None:
                    # there is letter in the date string
                    a_date_date = LetterMonthFinder(a_date, locale=self.locale).to_datetime()
                else:
                    a_date_date = NumberMonthFinder(a_date, locale=self.locale).to_datetime()

                if a_time == "":
                    a_time = "00:00:00"
                a_time_time = datetime.strptime(a_time, "%H:%M:%S").time()

                self.date = datetime.combine(a_date_date, a_time_time)

    def __repr__(self):
        return f"DateParser({self.date_in_str})"

    def to_datetime(self) -> datetime:
        return self.date

    def to_date(self) -> date:
        return self.date.date()

    def to_time(self) -> time:
        return self.date.time()

    def to_str(self, date_format: str = "%Y-%m-%d %H:%M:%S") -> str:
        return self.to_datetime().strftime(date_format)

    def to_date_str(self, date_format: str = "%Y-%m-%d") -> str:
        return self.to_date().strftime(date_format)

    def to_timestamp(self) -> float:
        return self.date.timestamp()

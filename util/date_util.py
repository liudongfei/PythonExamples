# -*- coding: utf-8 -*-
# @Time    : 2020/8/14 上午10:20
# @Author  : Mat
from pandas import isnull
import datetime as dt
from dateutil.parser import parse


class DateUtil:
    @staticmethod
    def datetime_to_datestring(dt):
        if isnull(dt):
            return None
        return dt.strftime("%Y-%m-%d")

    @staticmethod
    def datetime_to_datestring_format(dt, format='%Y-%m-%d'):
        if isnull(dt):
            return None
        return dt.strftime(format)

    @staticmethod
    def datestring_to_datetime(ds):
        if isnull(ds) or ds == '':
            return None
        return dt.datetime.strptime(ds, "%Y-%m-%d")

    @staticmethod
    def former_date(time=None, long=0):
        if time is None:
            time = dt.datetime.now()
        if isinstance(time, str):
            time = DateUtil.datestring_to_datetime(time)
        former = (time - dt.timedelta(days=long))
        str_time = former.strftime("%Y-%m-%d")
        return str_time

    @staticmethod
    def is_in_date_range_v2(date, start, end):
        if not isinstance(date, str):
            date = DateUtil.datetime_to_datestring(date)
        date = parse(date)
        if not isinstance(start, str):
            start = DateUtil.datetime_to_datestring(start)
        start = parse(start)
        if not isinstance(end, str):
            end = DateUtil.datetime_to_datestring(end)
        end = parse(end)
        index = dt.datetime(1990, 1, 1)
        start = (start - index).days
        end = (end - index).days
        point = (date - index).days
        if start <= point <= end:
            return True
        else:
            return False


if __name__ == '__main__':
    print(DateUtil.former_date())
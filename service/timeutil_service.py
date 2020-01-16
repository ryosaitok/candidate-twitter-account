# coding=utf-8
import time
from datetime import datetime, timedelta
from time import sleep


def current_datetime():
    return datetime.now()


def current_iso_formatted_datetime():
    return datetime.now().isoformat()


def jpy_formatted_current_datetime():
    """
    return japanese style formatted current datetime (ex. 2018年12月01日12時10分)
    """
    return datetime.now().strftime('%Y年%m月%d日 %H時%M分')


def slushed_current_datetime_without_second():
    """
    return japanese style formatted current datetime (ex. 2018/12/01 12:10)
    """
    return datetime.now().strftime('%Y/%m/%d %H:%M')


def slushed_datetime_without_second(datetime):
    """
    return japanese style formatted datetime (ex. 2018/12/01 12:10)
    """
    return datetime.strftime('%Y/%m/%d %H:%M')


def slushed_current_datetime():
    """
    return japanese style formatted current datetime (ex. 2018/12/01 12:10:00)
    """
    return datetime.now().strftime('%Y/%m/%d %H:%M:%S')


def slushed_datetime(datetime):
    """
    return japanese style formatted datetime (ex. 2018/12/01 12:10:00)
    """
    return datetime.strftime('%Y/%m/%d %H:%M:%S')


def iso_formatted_datetime(datetime):
    """
    return japanese style formatted datetime (ex. 2018-12-01T12:10:00)
    """
    return datetime.strftime('%Y-%m-%dT%H:%M:%S')


def jpy_formatted_date(datetime):
    """
    :param datetime: (ex. 2017-09-10 22:13:47.289211)
    return japanese style formatted current date (ex. 2018年12月1日)
    """
    return datetime.strftime('%Y年%-m月%-d日')


def jpy_formatted_current_date():
    """
    return japanese style formatted current date (ex. 2018年12月1日)
    """
    return datetime.now().strftime('%Y年%-m月%-d日')


def jpy_formatted_year_month(datetime):
    """
    :param datetime: (ex. 2017-09-10 22:13:47.289211)
    return japanese style formatted year and month (ex. 2017年9月)
    """
    return datetime.strftime('%Y年%-m月')


def jpy_formatted_current_year_month():
    """
    return japanese style formatted current year month (ex. 2018年12月)
    """
    return datetime.now().strftime('%Y年%-m月')


def connected_date(datetime):
    """
    :param datetime: (ex. 2017-09-10 22:13:47.289211)
    return japanese style formatted current date (ex. 20181201)
    """
    return datetime.strftime('%Y%m%d')


def connected_current_date():
    """
    return japanese style formatted current date (ex. 20181201)
    """
    return datetime.now().strftime('%Y%m%d')


def jpy_formatted_month_date(datetime):
    """
    :param datetime: (ex. 2017-09-10 22:13:47.289211)
    return japanese style formatted current date without year (ex. 12月1日)
    """
    return datetime.strftime('%-m月%-d日')


def jpy_formatted_current_month_date():
    """
    return japanese style formatted current date without year (ex. 12月1日)
    """
    return datetime.now().strftime('%-m月%-d日')


def slush_formatted_current_date():
    """
    return japanese style formatted current date (ex. 2018/12/01)
    """
    return datetime.now().strftime('%Y/%m/%d')


def slush_formatted_date(datetime):
    """
    :param datetime: (ex. 2017-09-10 22:13:47.289211)
    return japanese style formatted current date (ex. 2018/12/01)
    """
    return datetime.strftime('%Y/%m/%d')


def slush_formatted_month_date(datetime):
    """
    :param datetime: (ex. 2017-09-10 22:13:47.289211)
    return japanese style formatted current date (ex. 12/01)
    """
    return datetime.strftime('%Y/%m')


def kebab_formatted_date(datetime):
    """
    :param datetime: (ex. 2017-09-10 22:13:47.289211)
    return kebab style formatted date (ex. 2018-12-01)
    """
    return datetime.strftime('%Y-%m-%d')


def kebab_formatted_reverse_date(datetime):
    """
    :param datetime: (ex. 2017-09-10 22:13:47.289211)
    return kebab style reverse formatted date (ex. 01-12-2018)
    """
    return datetime.strftime('%d-%m-%Y')


def culc_after_year(year):
    """
    :param year: 年数（int）
    :return: 今から年数後の日付
    """
    return datetime.fromtimestamp(
        time.mktime((datetime.now().year + year, datetime.now().month, datetime.now().day, 0, 0, 0, 0, 0, 0)))


def culc_before_year(year):
    """
    :param year: 年数（int）
    :return: 今から年数前の日付
    """
    return datetime.fromtimestamp(
        time.mktime((datetime.now().year - year, datetime.now().month, datetime.now().day, 0, 0, 0, 0, 0, 0)))


def culc_after_month(month):
    """
    :param month: 月数（int）
    :return: 今から月数後の日付
    TODO:月ごとの日数の考慮できてない!!
    """
    return datetime.fromtimestamp(
        time.mktime((datetime.now().year, datetime.now().month + month, datetime.now().day, 0, 0, 0, 0, 0, 0)))


def culc_before_month(month):
    """
    :param month: 月数（int）
    :return: 今から月数前の日付
    TODO:月ごとの日数の考慮できてない!!
    """
    return datetime.fromtimestamp(
        time.mktime((datetime.now().year, datetime.now().month - month, datetime.now().day, 0, 0, 0, 0, 0, 0)))


def add_day(day):
    """
    :param day: 日数（int）
    :return: 今から日数後の日付
    """
    return datetime.now() + timedelta(days=day)


def minus_day(day):
    """
    :param day: 日数（int）
    :return: 今から日数前の日付
    """
    return datetime.now() - timedelta(days=day)


def add_hour(hour):
    """
    :param hour: 時間（int）
    :return: 今から指定時間後の日付
    """
    return datetime.now() + timedelta(hours=hour)


def minus_hour(hour):
    """
    :param hour: 時間（int）
    :return: 今から指定時間前の日付
    """
    return datetime.now() - timedelta(hours=hour)


def add_hour_from(dt, hour):
    """
    :param dt: 指定日時(datetime)
    :param hour: 時間（int）
    :return: 今から指定時間後の日付
    """
    return dt + timedelta(hours=hour)


def minus_hour_from(dt, hour):
    """
    :param dt: 指定日時(datetime)
    :param hour: 時間（int）
    :return: 今から指定時間前の日付
    """
    return dt - timedelta(hours=hour)


def add_minutes(minutes):
    """
    :param minutes: 分（int）
    :return: 今から指定分後の日付
    """
    return datetime.now() + timedelta(minutes=minutes)


def minus_minutes(minutes):
    """
    :param minutes: 分（int）
    :return: 今から指定分前の日付
    """
    return datetime.now() - timedelta(minutes=minutes)


def add_minutes_from(dt, minutes):
    """
    :param dt: 指定日時(datetime)
    :param minutes: 分（int）
    :return: 今から指定分後の日付
    """
    return dt + timedelta(minutes=minutes)


def minus_minutes_from(dt, minutes):
    """
    :param dt: 指定日時(datetime)
    :param minutes: 時間（int）
    :return: 今から指定分前の日付
    """
    return dt - timedelta(minutes=minutes)


def convert_to_jst(utc_dt):
    """
    :param utc_dt: UTCでの指定日時(datetime)
    :return: JSTでの日時
    """
    return utc_dt + timedelta(hours=9)


def get_todays_day_of_week_jp():
    """
    :return: 曜日（ex. 火曜日）
    """
    day_of_week_list = ['日曜日', '月曜日', '火曜日', '水曜日', '木曜日', '金曜日', '土曜日']
    return day_of_week_list[int(current_datetime().strftime('%w'))]


def get_day_of_week_jp(datetime):
    """
    :param datetime: 日時 (ex. 2017-09-10 22:13:47.289211)
    :return: 曜日（ex. 火曜日）
    """
    day_of_week_list = ['日曜日', '月曜日', '火曜日', '水曜日', '木曜日', '金曜日', '土曜日']
    return day_of_week_list[int(datetime.strftime('%w'))]


def format_jpy_week_count(datetime):
    """
    :param datetime: 日時 (ex. 2017-09-10 22:13:47.289211)
    :return: 日付（ex. 2018年12月 第1週目）
    """
    year = datetime.year
    month = datetime.month
    day = datetime.day
    week_num = 0
    while day > 0:
        week_num += 1
        day -= 7
    return '{}年{}月{}週目'.format(year, month, week_num)


def format_jpy_month_count(datetime):
    """
    :param datetime: 日時 (ex. 2017-09-10 22:13:47.289211)
    :return: 日付（ex. 2017年9月）
    """
    year = datetime.year
    month = datetime.month
    day = datetime.day
    week_num = 0
    while day > 0:
        week_num += 1
        day -= 7
    return '{}年{}月'.format(year, month)


def format_jpy_date(date_str):
    dt = datetime.strptime(date_str, "%Y-%m-%d")
    return jpy_formatted_date(dt)


def sleep_second(second):
    print('{}秒処理停止...'.format(second))
    sleep(second)

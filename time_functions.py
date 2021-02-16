# to manage current date
from datetime import datetime, timezone

def current_date_str():
    """
    gets today's date in UTC
    """
    # datetime object containing current date and time
    now = datetime.now(timezone.utc)
    # convert between timezones with pytz
    # return string with right format
    return now.strftime("%Y-%m-%d")

def current_datetime_str():
    """
    gets today's date and time in UTC
    """
    # datetime object containing current date and time
    now = datetime.now(timezone.utc)
    # convert between timezones with pytz
    # return string with right format
    return now.strftime("%Y-%m-%d %H:%M")

def current_time_str():
    """
    gets today's date and time in UTC
    """
    # datetime object containing current date and time
    now = datetime.now(timezone.utc)
    # convert between timezones with pytz
    # return string with right format
    return now.strftime("%H:%M")

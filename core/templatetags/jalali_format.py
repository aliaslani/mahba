import jdatetime
from django import template
from persiantools import characters, digits
from persiantools.jdatetime import JalaliDate, JalaliDateTime
import datetime
register = template.Library()



@register.filter
def g_to_j(date):
    if not date:
        return 'نامشخص'
    try:
        if isinstance(date, datetime.date) and not isinstance(date, datetime.datetime):
            date = datetime.datetime.combine(date, datetime.time.min)
        return JalaliDateTime(date).strftime("%Y/%m/%d")
    except Exception:
        return 'نامعتبر'

@register.filter
def fa_digits(value):
    try:
        return digits.en_to_fa(str(value))
    except Exception:
        return value

@register.filter
def fa_date(date):
    """ Full date conversion: Gregorian → Jalali + Persian digits """
    j_date = g_to_j(date)
    return fa_digits(j_date)
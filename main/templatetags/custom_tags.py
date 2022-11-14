from django import template

from riddlehouse.helpers import enums

register = template.Library()


def pagination_handle_pages(value, arg):
    if arg < 3:
        value = value[0:5]
    elif arg > len(value) - 3:
        number = (len(value) - arg)
        start = (arg - 5) + number
        end = arg + number
        value = value[start:end]
    else:
        value = value[arg - 3:arg + 2]
    return value


def convert_iso_to_weekday(day_number):
    if day_number == 1:
        return "شنبه"
    if day_number == 2:
        return "یک شنبه"
    if day_number == 3:
        return "دوشنبه"
    if day_number == 4:
        return "سه شنبه"
    if day_number == 5:
        return "چهارشنبه"
    if day_number == 6:
        return "پنج شنبه"
    if day_number == 7:
        return "جمعه"


register.filter('pagination_handle_pages', pagination_handle_pages)
register.filter('convert_iso_to_weekday', convert_iso_to_weekday)

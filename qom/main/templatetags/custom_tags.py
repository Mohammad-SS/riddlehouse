from django import template
from riddlehouse.helpers import functions, enums
import itertools
from main import models as main_models

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


def overview_handler(value: dict):
    _list = list()
    for k, v in value.items():
        _list.append(v)

    result = {
        "rooms": _list,
        "dates": [{"weekday": item.get('weekday'), "date": item.get('date')} for item in _list[0].get('calendar')]
    }

    return result


def overview_get_detail(value):
    room_data = dict()
    hour_big_list = [[k for k, v in item.get('hours').items()] for item in value.get('calendar')]
    hour_list = list(set(itertools.chain(*hour_big_list)))
    hour_list.sort()
    for hour in hour_list:
        detail = list()
        for t in value.get('calendar'):
            hour_obj = t.get('hours').get(hour)
            if hour_obj is not None:
                hour_obj.update({'date': t.get('date')})
            detail.append(hour_obj)
        room_data.update({hour: detail})
    return room_data


def load_landing_context(part: str, offset: str = "main", tag="", from_settings=False):
    if from_settings:
        try:
            setting = enums.DefaultSettings[f"{part}"]
            return functions.get_setting(setting, "")
        except Exception:
            return ""
    try:
        if not tag == "":
            tag = "_" + tag
        slug = f"{part}_{offset}{tag}"
        context = main_models.Context.objects.get(slug=slug)
        return context.value
    except Exception:
        return ""


def exclude_hours(exclusion):
    default_hours = exclusion.room.default_hours
    default_days = exclusion.room.default_days
    minus_hours = []
    minus_days = []
    additional_hours = []
    additional_days = []

    for hour in exclusion.hours:
        if hour not in default_hours:
            additional_hours.append(hour)
    for day in exclusion.weekdays:
        if day not in default_days:
            additional_days.append(day)
    for hour in default_hours:
        if hour not in exclusion.hours:
            minus_hours.append(hour)
    for day in default_days:
        if day not in exclusion.weekdays:
            minus_days.append(day)

    return {
        "min_days": minus_days,
        "min_hours": minus_hours,
        "add_days": additional_days,
        "add_hours": additional_hours
    }


register.filter('exclude_hours', exclude_hours)
register.filter('pagination_handle_pages', pagination_handle_pages)
register.filter('convert_iso_to_weekday', convert_iso_to_weekday)
register.filter('overview_handler', overview_handler)
register.filter('overview_get_detail', overview_get_detail)

register.simple_tag(load_landing_context, name="get_context")

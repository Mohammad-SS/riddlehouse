from django import template

from riddlehouse.helpers import enums

import itertools

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


def overview_handler(value:dict):
    _list = list()
    for k, v in value.items():
        _list.append(v)
    
    result = {
        "rooms": _list,
        "dates": [{"weekday":item.get('weekday'), "date":item.get('date')} for item in _list[0].get('calendar')]
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
        
        

register.filter('pagination_handle_pages', pagination_handle_pages)
register.filter('convert_iso_to_weekday', convert_iso_to_weekday)
register.filter('overview_handler', overview_handler)
register.filter('overview_get_detail', overview_get_detail)

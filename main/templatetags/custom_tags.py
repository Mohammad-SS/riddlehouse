from django import template

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


def get_setting_value(name):
    print(name)
    return None


register.filter('pagination_handle_pages', pagination_handle_pages)
register.filter('get_setting_value', get_setting_value)

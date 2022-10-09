from main import models as main_models
from django.core import exceptions


def get_setting(setting, default):
    setting_slug = setting.value.get("slug", None)
    if not setting_slug:
        return default

    setting_default = setting.value.get("default", None)
    if not setting_default:
        setting_default = default
    print(setting_default)
    try:
        return main_models.Setting.objects.get(slug=setting_slug).value
    except exceptions.ObjectDoesNotExist:
        return setting_default

from django.contrib.sitemaps import Sitemap

from .models import Room


class RoomSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.9

    def items(self):
        return Room.objects.all()

    def lastmod(self, obj):
        return obj.modified_time

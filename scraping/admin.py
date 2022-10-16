from django.contrib import admin
from scraping.models import Brand, Hardware, SiteInfo

# # Register your models here.
admin.site.register(Brand)
admin.site.register(Hardware)
admin.site.register(SiteInfo)
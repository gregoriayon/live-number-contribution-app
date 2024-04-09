from django.contrib import admin
from app_number.models import (
    Statistic,
    DataItem
)

# Register your models here.
admin.site.site_header = "Live Number Contribution App"

admin.site.register(Statistic)
admin.site.register(DataItem)

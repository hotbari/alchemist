from django.contrib import admin
from .models import Tier

class TierAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'match_type')

admin.site.register(Tier, TierAdmin)
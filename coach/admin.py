from django.contrib import admin
from .models import Coach
from users.models import CustomUser

# 어드민에서 코치 보여주는 것 커스텀

class CoachAdmin(admin.ModelAdmin):
    list_display = ('id', 'club', 'user')

    def username(self, obj):
        return obj.user.username

    username.admin_order_field = 'user'  # Allows column order sorting

admin.site.register(Coach, CoachAdmin)

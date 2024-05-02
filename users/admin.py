from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('phone', 'gender', 'birth')  # 실제 CustomUser 모델의 필드를 반영
    ordering = ('phone',)  # 실제 CustomUser 모델의 USERNAME_FIELD를 사용
    

# 장고 어드민 사이트에 CustomUser 모델을 CustomUserAdmin 설정으로 등록
admin.site.register(CustomUser, CustomUserAdmin)

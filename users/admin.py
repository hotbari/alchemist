from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    #add_form_template = 'admin/auth/user/add_form.html'
    # 필드셋 정의
    fieldsets = (
        *UserAdmin.fieldsets,  # 기본 필드셋을 가져옴
        (                       # 커스텀 필드 추가
            'Custom Fields',
            {
                'fields': (
                    'gender',
                    'birth',
                    'phone',
                    'auth',
                    'club',
                    'team',
                    'image_url',
                    'tier',
                )
            },
        ),
    )
    # 리스트 뷰 화면에서 보여줄 필드들 
    list_display = ['username', 'email', 'gender', 'birth', 'is_staff']

# 장고 어드민 사이트에 CustomUser 모델을 CustomUserAdmin 설정으로 등록
admin.site.register(CustomUser, CustomUserAdmin)

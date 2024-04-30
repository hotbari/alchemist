from django.db import models


class TimeStampedModel(models.Model): # 테이블에 생성시간 , 수정시간 기능을 넣어주기 위한 공통 모델
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True



class SoftDeleteModel(models.Model): # soft delete 모델 (레코드를 실제로 데이터베이스에서 삭제하지 않고, 삭제된 것으로 표시하여 나중에 복구할 수 있는 기능을 구현할 수 있음)
    is_deleted = models.BooleanField(default=False) # 대회 생성했다가 삭제, 경기기록 삭제, 유저 탈퇴, admin 부분에서 삭제기능 진행. (유저 삭제는 is_active 활용하여 비활성화로 돌리자)

    def delete(self, *args, **kwargs):
        self.is_deleted = True
        self.save()

    class Meta:
        abstract = True

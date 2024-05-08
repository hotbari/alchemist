import os
import boto3
from uuid import uuid4
from django.conf import settings

class S3ImageUploader:
    """S3에 이미지를 업로드하는 클래스"""
    
    @staticmethod
    def upload_image_to_s3(image_file):
        """S3에 이미지 파일을 업로드하고 URL, 확장자, 크기를 반환"""
        s3 = boto3.client('s3', aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                          aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY)
        bucket_name = settings.AWS_STORAGE_BUCKET_NAME
        _, extension = os.path.splitext(image_file.name)
        # 확장자 앞의 점(.)을 제거하여 순수 확장자만 반환하도록 수정
        extension = extension.lstrip('.')
        unique_file_name = f"{uuid4()}.{extension}"  # 파일명에 확장자 앞에 점(.) 추가
        s3.upload_fileobj(image_file, bucket_name, unique_file_name)

        image_url = f"https://{bucket_name}.s3.amazonaws.com/{unique_file_name}"
        file_size = image_file.size  # 파일 크기 추출

        return image_url, extension, file_size
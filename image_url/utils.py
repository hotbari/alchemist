import boto3
from django.conf import settings
from uuid import uuid4

class S3ImageUploader:
    def __init__(self, bucket_name=settings.AWS_STORAGE_BUCKET_NAME):
        self.s3 = boto3.client('s3',
                               aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                               aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY)
        self.bucket_name = bucket_name

    def upload_file(self, file):
        """
        S3 버킷에 파일을 업로드하고 업로드된 파일의 URL을 반환합니다.
        """
        file_name = f"{uuid4()}.{file.name.split('.')[-1]}"
        self.s3.upload_fileobj(
            file,
            self.bucket_name,
            file_name
        )
        file_url = f"https://{self.bucket_name}.s3.amazonaws.com/{file_name}"
        return file_url, file_name.split('.')[-1], file.size
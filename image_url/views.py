from rest_framework.views import APIView
from rest_framework.response import Response
from .models import ImageUrl
from .serializers import ImageUrlSerializer
from .utils import S3ImageUploader
from django.core.files.storage import FileSystemStorage

# 임시 파일 저장소를 위한 커스텀 스토리지 클래스
class InMemoryUploadStorage(FileSystemStorage):
    """데이터베이스에 저장되지 않는 임시 파일 저장소"""
    def get_available_name(self, name, max_length=None):
        return name

class ImageUploadView(APIView):
    def post(self, request, *args, **kwargs):
        image_file = request.FILES.get('image_file')
        if image_file:
            # 임시 저장소에 파일 저장
            temp_storage = InMemoryUploadStorage()
            temp_file = temp_storage.save(image_file.name, image_file)
            temp_file_path = temp_storage.path(temp_file)

            # 검증 후 S3에 업로드
            image_url, extension, file_size = S3ImageUploader.upload_image_to_s3(image_file)
            image_record = ImageUrl.objects.create(image_url=image_url, extension=extension, size=file_size)
            serializer = ImageUrlSerializer(image_record)

            # 임시 파일 삭제
            temp_storage.delete(temp_file)

            return Response(serializer.data, status=201)
        return Response({"error": "No image file provided"}, status=400)

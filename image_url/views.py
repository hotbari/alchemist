from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import ImageUploadSerializer
from .utils import S3ImageUploader




class ImageUploadView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = ImageUploadSerializer(data=request.data)
        if serializer.is_valid():
            image_file = request.FILES.get('image_url')
            if image_file:
                # S3Uploader 클래스의 인스턴스를 생성
                uploader = S3ImageUploader()

                # 해당 인스턴스를 사용하여 파일 업로드
                file_url, extension, size = uploader.upload_file(image_file)
                
                # S3로부터 받은 URL, 확장자, 파일 크기 정보 업데이트
                serializer.save(image_url=file_url, extension=extension, size=size)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response({"error": "No image file provided"}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
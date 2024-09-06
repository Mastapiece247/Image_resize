from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import status
from django.conf import settings
from django.core.files.storage import default_storage
from PIL import Image
from .models import ImageUpload
from .serializers import ImageUploadSerializer
import os

# Create your views here.


class ImageUploadView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):
        serializer = ImageUploadSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            image_instance = serializer.instance

            image_path = image_instance.image.path
            image = Image.open(image_path)

            image = image.resize((300, 300))
            image.save(image_path)

            return Response(
                {
                    "message": "Image uploaded and resized successfully.",
                    "image_url": request.build_absolute_uri(image_instance.image.url),
                },
                status=status.HTTP_201_CREATED,
            )
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

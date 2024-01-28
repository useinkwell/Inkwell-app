from django.test import TestCase

# Create your tests here.

# import json
# from django.conf import settings
# from django.http import JsonResponse
# from django.views.decorators.csrf import requires_csrf_token
# import os

# Static/Media
# from django.core.files.storage import FileSystemStorage


# @requires_csrf_token
# def upload_image_view(request):
#     try:
#         # Check if the request contains the 'image' file
#         if 'image' not in request.FILES:
#             raise ValueError("No file provided in the 'image' field.")

#         request_file_object = request.FILES['image']

#         # Check if the file type is allowed (adjust content_types accordingly)
#         allowed_content_types = ['image/jpeg', 'image/png']
#         if request_file_object.content_type not in allowed_content_types:
#             raise ValueError(f"Invalid file type. Allowed types: {', '.join(allowed_content_types)}")

#         file_storage = FileSystemStorage()

#         # Use os.path.splitext to separate the filename and extension
#         file_name, file_extension = os.path.splitext(request_file_object.name)

#         # Ensure a unique filename by appending a timestamp or using other strategies
#         stored_file = file_storage.save(f"{file_name}_{str(int(time.time()))}{file_extension}", request_file_object)

#         file_url = file_storage.url(stored_file)

#         return JsonResponse({"success": 1, "file": file_url})
#     except Exception as e:
#         return JsonResponse({"success": 0, "error": str(e)})

import os
from django.conf import settings

def file_path(request):
    file = request.FILES['file']
    path = os.path.join("uploads", file.name)
    with open(path, "wb") as fp:
        fp.write(file.read()) 
    return path

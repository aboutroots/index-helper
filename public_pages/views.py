from django.shortcuts import render
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from indexing.index_parser import IndexParser
from django.http import JsonResponse
import os

# Create your views here.
def index(request):
    if request.method == 'POST' and request.FILES['my_file']:
        myfile = request.FILES['my_file']
        fs = FileSystemStorage()

        with IndexParser() as _:
            fs.save("index.txt", myfile)
    
        data = {
            'uploaded_file_url': settings.MEDIA_URL + 'index.txt'
        }
        return JsonResponse(data)

    return render(request, 'index.html')


def rules(request):
    return render(request, 'rules.html')



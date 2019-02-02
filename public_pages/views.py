from django.shortcuts import render
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from indexing.parser import IndexParser
import os

# Create your views here.
def index(request):
    # import ipdb; ipdb.set_trace();
    if request.method == 'POST' and request.FILES['my_file']:
        myfile = request.FILES['my_file']
        fs = FileSystemStorage()

        with IndexParser() as _:
            fs.save("index.txt", myfile)
    
        return render(request, 'index.html', {
            'uploaded_file_url': '/media/index.txt'
        })
    return render(request, 'index.html')


def rules(request):
    return render(request, 'rules.html')



from django.shortcuts import render
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from indexing.parser import IndexParser


# Create your views here.
def index(request):
    if request.method == 'POST' and request.FILES['my_file']:
        myfile = request.FILES['my_file']
        fs = FileSystemStorage()
        filename = fs.save("index.txt", myfile)
        uploaded_file_url = fs.url(filename)

        parser = IndexParser()
        parser.parse()
    
        return render(request, 'index.html', {
            'uploaded_file_url': uploaded_file_url
        })

    return render(request, 'index.html')

def rules(request):
    context = {}
    return render(request, 'rules.html', context=context)



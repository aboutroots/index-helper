from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.http import JsonResponse
from django.shortcuts import render

from indexing.index_parser import IndexParser


# Create your views here.
def index(request):
    if request.method == 'POST' and request.FILES['my_file']:
        myfile = request.FILES['my_file']
        fs = FileSystemStorage()

        try:
            with IndexParser() as _:
                fs.save("index.txt", myfile)
        except (AttributeError, AssertionError) as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            })

        return JsonResponse({
            'success': True,
            'uploaded_file_url': settings.MEDIA_URL + 'index.txt'
        })

    return render(request, 'index.html')


def rules(request):
    return render(request, 'rules.html')

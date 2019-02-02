from django.conf import settings
import os
class IndexParser:
    PATH = os.path.join(settings.MEDIA_ROOT, "index.txt")

    def __enter__(self):
        # to overwrite index file
        if os.path.exists(self.PATH):
            os.remove(self.PATH) 
    
    def __exit__(self, exc_type, exc_value, exc_traceback):
        with open (self.PATH, 'a') as file:
            file.write("TEST")

        
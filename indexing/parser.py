from django.conf.global_settings import MEDIA_ROOT
class IndexParser:
    def __init__(self):
        self.PATH = MEDIA_ROOT + "index.txt"

    def parse(self):
        with open (self.PATH, 'a') as file:
            file.write("TEST")
        


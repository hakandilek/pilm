from django.template import Context, loader
from pilm.models import File
from django.http import HttpResponse

def home(request):
    t = loader.get_template('home.html')
    c = Context()
    return HttpResponse(t.render(c))
    
def import_files(request):
    t = loader.get_template('import_files.html')
    c = Context()
    return HttpResponse(t.render(c))
    
def list_files(request):
    t = loader.get_template('list_files.html')
    c = Context()
    return HttpResponse(t.render(c))    

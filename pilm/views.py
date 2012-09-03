from django.template import Context, loader
from pilm.models import File, Pack, Movie
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.views.generic.list_detail import object_list
from django.views.generic.create_update import delete_object
from django.utils.translation import ugettext as _
from pilm.tasks import QueryThread, import_files
import logging
# Get an instance of a logger
log = logging.getLogger(__name__)

def home(request):
    t = loader.get_template('pilm/home.html')
    context=Context()
    context["title"] = _('home')
    return HttpResponse(t.render(context))
    
def file_index(request, context={}):
    log.debug('file_index <-')
    
    q = File.objects.all().order_by('name')

    # Make sure page request is an int. If not, deliver first page.
    try:
        pagenum = int(request.GET.get('page', '1'))
    except ValueError:
        pagenum = 1
    log.debug('pagenum : %d' % pagenum)

    for f in q:
        log.debug("file:%s" % f.name)
            
    context["title"] = _('files')
    context['result_headers'] = [
                                 {'text'  : _('name'), },
                                 {'text'  : _('delete'), },
                                 ]
    return object_list(request, q, page=pagenum, paginate_by=10, template_name='pilm/file_list.html', extra_context=context)

def file_create(request):
    if request.method == 'POST':
        #do save
        files = request.POST['files'].splitlines()
        import_files(files)
        
        return HttpResponseRedirect(reverse('pilm.views.file_index'))
    else: 
        return HttpResponse(_("invalid request."))

def file_edit(request, name=None):
    context = {
               'name' : name,
    }
    return file_index(request, context);

def file_delete(request, name=None):
    return delete_object(request, File, object_id=name,
                         post_delete_redirect=reverse('pilm.views.file_index'))

def pack_index(request, context={}):
    log.debug('pack_index <-')
    
    q = Pack.objects.all().order_by('query')

    # Make sure page request is an int. If not, deliver first page.
    try:
        pagenum = int(request.GET.get('page', '1'))
    except ValueError:
        pagenum = 1
    log.debug('pagenum : %d' % pagenum)

    context["title"] = _('movies')
    context['result_headers'] = [
                                 {'text'  : _('name'), },
                                 {'text'  : _('status'), },
                                 ]
    return object_list(request, q, page=pagenum, paginate_by=10, template_name='pilm/pack_list.html', extra_context=context)

def query(request, key=None):
    try:
        p = Pack.objects.get(key=key)
    except Pack.DoesNotExist:
        raise Http404
    
    p.queryStatus = 'I'
    p.save()
    
    q = QueryThread([p])
    q.start()
    
    context = {}
    return pack_index(request, context);

def assign(request, pack_key=None, movie_key=None):
    try:
        pack = Pack.objects.get(key=pack_key)
    except Pack.DoesNotExist:
        raise Http404("pack not found: %s" % pack_key)
    try:
        movie = Movie.objects.get(key=movie_key)
    except Movie.DoesNotExist:
        raise Http404("movie not found: %s" % movie_key)

    pack.name = movie.title
    pack.assignedMovie = movie
    pack.queryStatus='A'
    
    pack.save()
    context = {}
    return pack_index(request, context)

def movie_index(request, context={}):
    log.debug('movie_index <-')
    
    q = Movie.objects.all().order_by('title')

    # Make sure page request is an int. If not, deliver first page.
    try:
        pagenum = int(request.GET.get('page', '1'))
    except ValueError:
        pagenum = 1
    log.debug('pagenum : %d' % pagenum)

    for f in q:
        log.debug("movie:%s" % f.title)
            
    context["title"] = _('movies')
    context['result_headers'] = [
                                 {'text'  : _('title'), },
                                 {'text'  : _('delete'), },
                                 ]
    return object_list(request, q, page=pagenum, paginate_by=10, template_name='pilm/movie_list.html', extra_context=context)#TODO:template

def movie_show(request, key=None):
    #TODO:get/show/template
    pass


from django.template import Context, loader
from pilm.models import File
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic.list_detail import object_list
from django.views.generic.create_update import delete_object
from django.utils.translation import ugettext as _
import logging
# Get an instance of a logger
logger = logging.getLogger(__name__)

def home(request):
    t = loader.get_template('pilm/home.html')
    context=Context()
    context["title"] = _('home')
    return HttpResponse(t.render(context))
    
def file_index(request, context={}):
    logger.debug('file_index <-')
    
    q = File.objects.all().order_by('name')

    # Make sure page request is an int. If not, deliver first page.
    try:
        pagenum = int(request.GET.get('page', '1'))
    except ValueError:
        pagenum = 1
    logger.debug('pagenum : %d' % pagenum)

    for f in q:
        logger.debug("file:%s" % f.name)
            
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
        for name in files:
            f = File(name=name)
            logger.debug('name    : %r' % name)
            new_object = f.save()
            logger.debug('new_object    : %r' % new_object)
        
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

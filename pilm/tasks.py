from threading import Thread
from pilm.query import search_movie 
from pilm.models import Movie, File, Pack
from pilm.query import refine
import logging
from django.db.utils import IntegrityError
# Get an instance of a logger
log = logging.getLogger(__name__)

class QueryThread(Thread):

    def __init__(self, packs):
        Thread.__init__(self)
        self.packs = packs
    
    def run(self):
        #do query here
        for pack in self.packs:
            log.info("query: %s" % pack.query)
            movies = search_movie(pack.query)
            #assign movies into pack
            movielist=[]
            for m in movies:
                title=m['title']
                iid=m.movieID
                log.info("imdbID:%s title:%s" % (iid, title))
                movie = Movie(title=title, imdbId=iid)
                try:
                    movie.save()
                    movielist.append(movie)
                except IntegrityError:
                    log.info("skip already existing movie: %s" % movie)

            #associate movie & pack
            for movie in movielist:
                pack.movies.add(movie)
            
            #change status
            pack.status = 'P'
            
            #save movie pack
            pack.save()

class FileImportThread(Thread):
    
    def __init__(self, filelist):
        Thread.__init__(self)
        self.filelist = filelist
    
    def run(self):
        for name in self.filelist:
            q = refine(name)
            p = Pack(query=q)
            log.debug('name    : %r' % name)
            p.save()
            f = File(name=name, pack=p)
            f.save()
            log.debug('p    : %s' % p)
            log.debug('f    : %s' % f)
            log.debug('f.pack.key: %s' % f.pack.key)
            
def import_files(files, thread=True):
    t = FileImportThread(files)
    if thread:
        t.start()
    else:
        t.run()
    

def query_all_new(thread=True):
    packs = Pack.objects.filter(queryStatus='N')
    t = QueryThread(packs)
    if thread:
        t.start()
    else:
        t.run()

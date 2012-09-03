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
                log.info("imdbID:%s title:%s" % (m.movieID, m['long imdb title']))
                log.debug(" keys:%s" % m.keys())
                rating = m.get('rating')
                imdbId=m.movieID
                movie = Movie(imdbId=imdbId, title=m['long imdb title'], year=m['year'], kind=m['kind'], rating=rating)
                try:
                    movie.save()
                except IntegrityError as e:
                    log.info("skip already existing movie: %s - %s" % (movie, e))
                    movie = Movie.objects.get(imdbId=imdbId)
                if movie:
                    movielist.append(movie)

            #associate movie & pack
            for movie in movielist:
                pack.movies.add(movie)
            
            #change status
            pack.queryStatus = 'P'
            
            #save movie pack
            pack.save()

class FileImportThread(Thread):
    
    def __init__(self, filelist):
        Thread.__init__(self)
        self.filelist = filelist
    
    def run(self):
        for name in self.filelist:
            name = name.rstrip()
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

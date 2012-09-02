# Get an instance of a logger
import logging
log = logging.getLogger(__name__)

#######################
# constant definitions
FILE_SPLITTERS = set(['[', ']', '(', ')', ' ', '-', '.'])
IGNORE_WORDS = ["avi", "mkv", "dts", "x264", "h264", "phd", "hd", "hdevo", "chd", "bdrip", "1080p", "720p", "480p", "multi", "highcode", "bluray","blueray", "multisub", "cd1", "dvdrip", "xvid", "ac3", "rf", "flac", "ea", "cd1", "cd2", "fre", "ger", "eng", "wiki", "hdchina", "esir", "ctrlhd", "ebp", "johno70", "amiable", "unrated", "dvdhd", "hddvd"]

#######################
# function definitions
def split_(parts, splitter):
    result=[]
    for part in parts:
        pp = part.split(splitter)
        result.extend(pp)
    return result
        
def split(parts, splitters):
    for splitter in splitters:
        result = split_(parts, splitter)
        log.debug("split %s :: %s = %s" %(parts, splitter, result))
        parts = result
    return parts
        
def refine(filename):
    log.debug("refine filename=%s" % filename)
    parts = split(set([filename]), FILE_SPLITTERS)
    log.debug("parts=%s" % parts)
    parts = filter(None, parts)
    parts[:] = [word.lower() for word in parts]
    parts[:] = [word for word in parts if word not in IGNORE_WORDS]
    result = ' '.join(parts)
    return result


from imdb import IMDb
i = IMDb('mobile')

def search_movie(query):
    return i.search_movie(query)
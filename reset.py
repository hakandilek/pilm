#!/usr/bin/env python
import os
# This is c.py
import logging

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "pilm.settings")
    
    # Make a global logging object.
    log = logging.getLogger()
    log.setLevel(logging.DEBUG)
    h = logging.StreamHandler()
    f = logging.Formatter("%(levelname)s %(asctime)s %(funcName)s %(lineno)d %(message)s")
    h.setFormatter(f)
    log.addHandler(h)

    #reset DB
    try:    
        os.remove('pilm.db')
    except OSError:
        log.info("ignore missing file: pilm.db")
    from django.core.management import call_command
    call_command('syncdb', interactive = False)
    
    #import file list
    log.info( "importing file list...")
    from pilm.tasks import import_files
    files = open('list.txt', 'r').readlines()
    import_files(files, thread=False)
    
    #query films from IMDB
    log.info("querying movies...")
    from pilm.tasks import query_all_new
    query_all_new(thread=False)
    
    

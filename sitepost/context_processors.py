from django.conf import settings

def common(request):
    """ Common context objects included on every page. We pass through True & False
    so we can use them "naturally" within templates. Maps are used on enough pages
    that better to just include the key here (or maybe move into template itself.
    """
    GMAPS_KEY = settings.GOOGLE_MAPS['API_KEY']
   # print 'googlemap key = %s' % GMAPS_KEY
    if not GMAPS_KEY or GMAPS_KEY == '':
        GMAPS_KEY = None
        print 'googlemap key = %s' % GMAPS_KEY
        
    return {
        'GMAPS_KEY' : GMAPS_KEY,       
    }

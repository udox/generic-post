# -*- coding: utf-8 -*-
#from ooyala.constants import OoyalaAPI
from django.conf import settings

#if hasattr(settings, 'OOYALA'):
#    API_KEYS = settings.OOYALA['API_KEYS']
#else:
#    raise Exception('Cannot import your Ooyala API keys from settings.py')

# Parameters, remappings and default values for each API type. The base class
# will use the data here to make sure only valid params are passed and it will
# also rename parameters from python style to the required schema defintion

# TODO: the label param should be able to take a list and then transformed into
# label[0..X] etc, for now we allow just 1 label search
"""
Social config
"""
FACEBOOK_LIKE = {   
    'IMAGE': 'http://a0.twimg.com/a/1287437169/images/twitter_logo_header.png',
    'FBADMINS': '100000670576512',    
}

TWITTER = {   
        'URL': 'http://url.com',
        'message': 'this is the title of some such post',   
}

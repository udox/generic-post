# -*- coding: utf-8 -*-
#from ooyala.constants import OoyalaAPI
from django.conf import settings

if hasattr(settings, 'OOYALA'):
    API_KEYS = settings.OOYALA['API_KEYS']
else:
    raise Exception('Cannot import your Ooyala API keys from settings.py')

# Parameters, remappings and default values for each API type. The base class
# will use the data here to make sure only valid params are passed and it will
# also rename parameters from python style to the required schema defintion

# TODO: the label param should be able to take a list and then transformed into
# label[0..X] etc, for now we allow just 1 label search
FACEBOOK_PARAMS = {
    FACEBOOK.LIKE: {
        'PARAMS': ['content_type', 'statistics', 'description', 'embed_code', 'fields', 'include_deleted', 'label', 'limit', 'page_id' , 'title'],
        'REMAPS': {'embed_code': 'embedCode', 'label': 'label[0]', 'content_type': 'contentType', 'page_id': 'pageID' },
        'DEFAULTS': {},
    }
}

# -*- coding: utf-8 -*-
from django.conf import settings

"""
Social config
"""
FACEBOOK_LIKE = {  
    # Facebook will resize image to 90x90px 
    'IMAGE': '',# 
    'FBADMINS': '',#100000670576512    
}

"""
Not actually being used at this time need object passed through on tag to generate
full url path and post title as the message
"""
TWITTER = {   
        'URL': 'http://url.com',
        'message': 'this is the title of some such post',   
}
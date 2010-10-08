# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from django.http import HttpResponse, Http404, HttpResponseRedirect, HttpResponseForbidden
from django.template import RequestContext
from django.shortcuts import get_object_or_404
from django.core import serializers
from django.utils import simplejson as json
from radio.models import Show, PodcastSeries, RadioSkin
from django.conf import settings

PLAYER_TITLE = None
PAGE_TITLE = 'Spine Radio'

if hasattr(settings, 'RADIO_PLAYER_TITLE'):
    PLAYER_TITLE = settings['RADIO_PLAYER_TITLE']
if hasattr(settings, 'RADIO_PAGE_TITLE'):
    PAGE_TITLE = settings['RADIO_PAGE_TITLE']

def showdump(request):
    """ Dumps out the show data as a JSON array for loading into other
    programs (flash maybe? :) """

    return_data = list()
    shows = Show.live.all()[:10]
    for show in shows:
        return_data.append({
            'pk': show.pk,
            'media': show.media.url,
            'image': 'img/shows/active-%s.png' % show.picture,
            'title': show.title,
            'description': show.description,
            'created': show.created_at.strftime('%d/%m/%y %H:%M'),
        })
    return HttpResponse(json.dumps(dict(shows=return_data)))

def player(request):
    skin = RadioSkin.get_active()
    context = {
        'page_title': PAGE_TITLE,
        'player_title': PLAYER_TITLE,
        'skin': skin,
    }
    return render_to_response('radio/container.html', context,
        context_instance=RequestContext(request))

def series(request, slug):
    skin = RadioSkin.get_active()
    context = {
        'page_title': PAGE_TITLE,
        'player_title': PLAYER_TITLE,
        'skin': skin,
        'slug': slug,
    }
    return render_to_response('radio/container.html', context,
        context_instance=RequestContext(request))

def embed(request, object_id):
    show = get_object_or_404(Show, pk=object_id)
    return HttpResponse(show.embed_code)

def download(request, object_id):
    show = get_object_or_404(Show, pk=object_id)
    if show.allow_download:
        return HttpResponseRedirect(show.absolute_media_url)
    else:
        return HttpResponseForbidden()

def playing(request, object_id):
    show = get_object_or_404(Show, pk=object_id)
    return HttpResponseRedirect(show.absolute_media_url)

def play(request, object_id):
    show = get_object_or_404(Show, pk=object_id)
    if show.media:
        return HttpResponse(json.dumps(dict(show=show.media.url)), mimetype='application/json')
    else:
        raise Http404

def get_bare_player(request, object_id):
    show = get_object_or_404(Show, pk=object_id)
    if show.media or show.media_url:
        return HttpResponse(show.flash_player)
    else:
        raise Http404

def podcast_xml(request, slug):
    podcast = get_object_or_404(PodcastSeries, url=slug)
    base_domain = 'http://www.spinetv.net' # HACKALERT! TODO: pull from sites
    return render_to_response('radio/podcast.xml', {'podcast': podcast, 'base_domain': base_domain },
        mimetype='text/xml')

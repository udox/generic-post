from django.db.models import Q, Manager

class LiveManager(Manager):
    """ A maanger for switchable objects ordered by descending created date """
    def get_query_set(self):
        return super(LiveManager, self).get_query_set().filter(status=5).order_by('-created_at')
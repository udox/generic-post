from django.db import models

"""
 via http://stackoverflow.com/questions/454436/unique-fields-that-allow-nulls-in-django
 allows us to have a slug field that can be null but also unique
 discussion on the original problem here: http://code.djangoproject.com/ticket/9039
"""

class SlugNullField(models.SlugField):
    description = "SlugField that stores NULL but returns ''"
    def to_python(self, value):  #this is the value right out of the db, or an instance
       if isinstance(value, models.SlugField): #if an instance, just return the instance
              return value
       if value==None:   #if the db has a NULL (==None in Python)
              return ""  #convert it into the Django-friendly '' string
       else:
              return value #otherwise, return just the value
    def get_db_prep_value(self, value):  #catches value right before sending to db
       if value=="":     #if Django tries to save '' string, send the db None (NULL)
            return None
       else:
            return value #otherwise, just pass the value
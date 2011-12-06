from django.db import models

class NewsSubmission(models.Model):
    user = models.CharField(max_length=255)
    email_address = models.CharField(max_length=1024)    
    submission = models.TextField()
    
    class Meta(object):
        app_label = "public"

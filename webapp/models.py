from django.db import models
from django.db.models import Q
import datetime

class Messages(models.Model):
    title = models.CharField(max_length=200, blank=False, unique=True)
    post_id = models.IntegerField(blank=False)
    post_url = models.TextField(blank=False,default='')
    post_category = models.CharField(max_length=200, blank=False)
    post_thumbnail = models.TextField( blank=False)
    post = models.TextField(blank=False)
    no_likes = models.CharField(max_length=100, blank=True)
    post_date = models.DateField()
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created']



def query_message_report_by_args(**kwargs):
    start_date = kwargs.get('start_date', None)
    end_date = kwargs.get('end_date', None)
    post_category = kwargs.get('post_category', None)
    no_likes = kwargs.get('no_likes', None)
 

    queryset = Messages.objects.all()

    if start_date and end_date:
        start_date=start_date[0]
        end_date=end_date[0]
        queryset=queryset.filter(
        Q(post_date__range=[start_date,end_date],
        )| Q(post_date__icontains=end_date))

    if post_category :
        post_category=post_category[0]
        queryset=queryset.filter(post_category=post_category)

    if no_likes :
        no_like=no_likes[0]
        print(no_like)
        queryset=queryset.filter(no_likes=no_like)
 

    return queryset

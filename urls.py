from django.conf.urls import patterns, include, url
from django_bigbluebutton.views import MeetingsView

urlpatterns = patterns(
    '',
    url(r'^', MeetingsView.as_view(), name='meetings'),
)

from django.conf.urls import patterns, include, url
from django.conf import settings

from django_bigbluebutton.views import MeetingSubscriptionView
from django_bigbluebutton.views import MeetingConnectionView
from django_bigbluebutton.views import MeetingsView

urlpatterns = patterns(settings.DJANGO_BBB_BASE_URL,
    url(r'^(\d+)/{}'.format(settings.DJANGO_BBB_SUBSCRIPTION_URL),
        MeetingSubscriptionView.as_view(), name='meeting_subscription'),
    url(r'^(\d+)/{}'.format(settings.DJANGO_BBB_CONNECTION_URL),
        MeetingConnectionView.as_view(), name='meeting_connection'),
    url(r'^', MeetingsView.as_view(), name='meetings'),
)

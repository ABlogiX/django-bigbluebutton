django_bigbluebutton
====================
A django application which allow django users to interact with a BigBlueButton server.
For this, i forked and update for python 3 compatibilty this wrapper : https://github.com/jamieforrest/python-bigbluebutton


FEATURES :
----------
- Create and delete meetings in django admin
- Consult, register and join meeting in a django CMS page (App Hook)
- Send mail when user register to a meeting
- Send mail to meeting's attendees

INSTALLATION :
--------------
In your settings.py :

- Add `'django_bigbluebutton'` to your INSTALLED_APPS.
- Add theses lines :
    - `BBB_SECRET = 'your_shared_secret'`
    - `BBB_URL = 'http://your_hostname/bigbluebutton/'`
    - `BBB_LOGOUT_URL = 'http://your_hostname'`
    - `DJANGO_BBB_BASE_URL = 'meetings'`
    - `DJANGO_BBB_SUBSCRIPTION_URL = 'subscription'`
    - `DJANGO_BBB_CONNECTION_URL = 'connection'`

- You also need to configure mail settings, see : https://docs.djangoproject.com/en/dev/topics/email/

In your urls.py :

- Put : `url(r'^{}/'.format(settings.DJANGO_BBB_BASE_URL), include('django_bigbluebutton.urls')),` and make sure it's before : `url(r'^', include('cms.urls')),` if you're using django cms.

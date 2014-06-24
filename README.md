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
- Put `'django_bigbluebutton'` to your INSTALLED_APPS.
- Add theses lines :
    - `BBB_SECRET = 'your_shared_secret'`
    - `BBB_URL = 'http://your_hostname/bigbluebutton/'`
    - `BBB_LOGOUT_URL = 'http://your_hostname'`
- You also need to configure mail settings, see : https://docs.djangoproject.com/en/dev/topics/email/

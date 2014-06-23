from django.db import models
from django.core.validators import MinValueValidator
from django.conf import settings
from django.db.models.signals import pre_delete
from django.dispatch.dispatcher import receiver

from cms.models import CMSPlugin

from django_bigbluebutton.bbb_api import getMeetings, createMeeting, endMeeting

def delete_meeting_in_bigbluebutton(sender, instance, *args, **kwargs):
    endMeeting(
        instance.unique_id, instance.moderator_pw,
        settings.BBB_URL, settings.BBB_SECRET
    )


class Meeting(models.Model):

    def get_unique_id():
        if Meeting.objects.all().count() == 0:
            return 1
        else:
            return Meeting.objects.latest('id').unique_id + 1

    name = models.CharField(max_length=50,)
    unique_id = models.IntegerField(
        unique=True,
        default=get_unique_id
    )
    attendee_pw = models.CharField(max_length=50, blank=True)
    moderator_pw = models.CharField(max_length=50, blank=True)
    welcome_message = models.CharField(max_length=200, blank=True)
    logout_url = models.URLField(default=settings.BBB_LOGOUT_URL)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        createMeeting(
            self.name, self.unique_id, self.welcome_message,
            self.moderator_pw, self.attendee_pw, self.logout_url,
            settings.BBB_URL, settings.BBB_SECRET
        )

        if self.moderator_pw == '' or self.attendee_pw == '':
            list_meetings = getMeetings(settings.BBB_URL, settings.BBB_SECRET)

            meetings = []

            if list_meetings is not None:
                if list_meetings['meetings'] is not None:
                    meetings = list(list_meetings['meetings'].values())

            for meeting in meetings:
                if int(meeting.get('meetingID')) == self.unique_id:
                    print(meeting.get('moderatorPW'))
                    self.moderator_pw = meeting.get('moderatorPW')
                    self.attendee_pw = meeting.get('attendeePW')

        super(Meeting, self).save(*args, **kwargs)

pre_delete.connect(delete_meeting_in_bigbluebutton, sender=Meeting)

class RegisteredUser(models.Model):
    mail = models.EmailField()
    last_name = models.CharField(max_length=50)
    first_name = models.CharField(max_length=50)
    company = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=40)
    meetings = models.ManyToManyField(Meeting)
    
    def __str__(self):
        return self.mail
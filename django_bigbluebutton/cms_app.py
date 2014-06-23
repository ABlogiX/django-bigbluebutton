from cms.app_base import CMSApp
from cms.apphook_pool import apphook_pool
from django.utils.translation import ugettext_lazy as _


class BigBlueButtonApp(CMSApp):
    name = _("BigBlueButton App")
    urls = ["django_bigbluebutton.urls"]

apphook_pool.register(BigBlueButtonApp)
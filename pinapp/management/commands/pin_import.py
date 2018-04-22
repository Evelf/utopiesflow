# coding: utf-8
import json

import requests
from django.conf import settings
from django.core.management.base import BaseCommand
from django.utils.http import urlencode

from pinapp.api_tools import APITools


class Command(BaseCommand):
    # todo: https://github.com/joestump/python-oauth2/wiki/Signing-A-Request
    help = 'Import pin(s) from Pinterest by id'

    def add_arguments(self, parser):
        parser.add_argument('pin_id',
                            type=int,
                            nargs='+',
                            help='Id of the pin to import')
        parser.add_argument('--override_image',
                          action='store_true',
                          default=False,
                          dest='override_image',
                          help='Override pin\'s image')

    @classmethod
    def get_url(cls, pin_id):
        params = {
            'access_token': settings.PINAPP_ACCESS_TOKEN,
            'fields': APITools.api_fields()
        }
        return "%s%s%s?%s" % (
            settings.PINAPP_BASE_URL, '/pins/', pin_id, urlencode(params))

    def handle(self, *args, **options):
        pin_ids = options['pin_id']
        override_image = options['override_image']

        for pin_id in pin_ids:
            url = self.get_url(pin_id)
            res = requests.get(url)
            if res.status_code != 200:
                self.stdout.write("%s KO: %s" % (url, res.status_code))
            else:
                content = json.loads(res.content)
                pin_data = content['data']
                self.stdout.write(repr(pin_data))
                APITools.update_pin(pin_data, override_image)

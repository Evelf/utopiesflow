# coding: utf-8
import json
import requests
from datetime import datetime

from django.conf import settings
from django.core.management.base import BaseCommand
from django.utils import timezone
from django.utils.http import urlencode

from pinapp.api_tools import APITools
from pinapp.models import Pin


class Command(BaseCommand):
    # todo: https://github.com/joestump/python-oauth2/wiki/Signing-A-Request
    help = 'Import pins from Pinterest'

    def add_arguments(self, parser):
        parser.add_argument('-c',
                          '--cursor',
                          action='store',
                          dest='cursor',
                          help='Cursor for the next fetch')
        parser.add_argument('-l',
                          '--limit',
                          action='store',
                          type=int,
                          dest='limit',
                          help='Limit for the next fetch')

    @classmethod
    def get_url(cls, cursor=None, limit=None):
        params = {
            'access_token': settings.PINAPP_ACCESS_TOKEN,
            'limit': 50,
            'fields': APITools.api_fields()
        }
        if cursor:
            params.update({'cursor': cursor})
        if limit:
            params.update({'limit': limit})
        return "%s%s?%s" % (
            settings.PINAPP_BASE_URL, '/me/pins/', urlencode(params))

    def handle(self, *args, **options):
        cursor = options['cursor']
        limit = options['limit']

        last_sync_at = Pin.objects.values(
            'sync_at').latest('sync_at')['sync_at']
        earlier_pin = datetime.now(timezone.utc)
        nb_done = 0
        while (earlier_pin > last_sync_at):
            res = requests.get(self.get_url(cursor, limit))
            if res.status_code != 200:
                self.stdout.write("%s: %s" % ('KO', res.status_code))
                self.stdout.write("Last cursor: %s" % (cursor))
            else:
                content = json.loads(res.content)
                data = content['data']
                self.stdout.write(repr(data))

                for pin_data in data:
                    pin_created_at = APITools.update_pin(pin_data)
                    earlier_pin = min(earlier_pin, pin_created_at)
                    nb_done += 1

                cursor = content['page']['cursor']
                self.stdout.write(cursor)
        self.stdout.write("Previous sync: %s" % (last_sync_at))
        self.stdout.write("Earlier_created_at: %s" % (earlier_pin))
        self.stdout.write("Nb done: %s" % (nb_done))
        self.stdout.write("Last cursor: %s" % (cursor))

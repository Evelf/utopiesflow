# coding: utf-8
import requests
import json

from django.conf import settings
from django.core.management.base import BaseCommand
from django.utils.http import urlencode

from pinapp.api_tools import APITools


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
        parser.add_argument('-r',
                          '--rounds',
                          action='store',
                          type=int,
                          dest='rounds',
                          help='Number of fetch rounds')

    @classmethod
    def get_url(cls, cursor=None, limit=None):
        params = {
            'access_token': settings.PINAPP_ACCESS_TOKEN,
            'limit': 5,
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
        rounds = options['rounds'] or 1
        for i in range(0, rounds):
            res = requests.get(self.get_url(cursor, limit))
            if res.status_code != 200:
                self.stdout.write("%s: %s" % ('KO', res.status_code))
            else:
                content = json.loads(res.content)
                data = content['data']
                self.stdout.write(repr(data))

                for pin_data in data:
                    APITools.update_pin(pin_data)

                cursor = content['page']['cursor']
                self.stdout.write(cursor)

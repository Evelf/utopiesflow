# coding: utf-8

from __future__ import unicode_literals

import json
import sqlite3
from time import sleep

import requests
from django.conf import settings
from django.core.management.base import BaseCommand
from django.utils.http import urlencode
from requests.exceptions import SSLError, TooManyRedirects

from pinapp.api_tools import APITools
from pinapp.models import Pin


class Command(BaseCommand):
    help = 'Get the true source url from pins'

    def add_arguments(self, parser):
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
        parser.add_argument('-s',
                          '--sleep',
                          action='store',
                          type=int,
                          dest='sleep_time',
                          help='Time to sleep in secondes')

    @classmethod
    def steal_session_cookies(cls):
        conn = sqlite3.connect(settings.BROWSER_SESSION_FILE)
        c = conn.cursor()
        cookie_names = ['_pinterest_sess']
        cookies = {}
        for c_name in cookie_names:
            t = ('pinterest.fr', c_name)
            c.execute(
                'select value from moz_cookies'
                ' where baseDomain=?'
                ' and name=?;', t)
            cookie_value, = c.fetchone()
            cookies[c_name] = cookie_value
        conn.close()
        return cookies

    def handle(self, *args, **options):
        limit = options['limit']
        rounds = options['rounds'] or 1
        sleep_time = options['sleep_time'] or 1
        cookies = self.steal_session_cookies() 
        session = requests.Session()
        # session.max_redirects = 1
        for i in range(0, rounds):
            pins = Pin.objects.filter(
                    true_source_url__isnull=True
                ).exclude(source_url='')
            for pin in pins.iterator():
                print pin.id
                print pin.pin_url
                print pin.source_url
                sleep(sleep_time)
                try:
                    target_page = session.head(
                        pin.source_url,
                        cookies=cookies,
                        allow_redirects=True)
                # except SSLError:
                except TooManyRedirects:
                    print target_page.history
                    break
                # requests.exceptions.ConnectionError: HTTPConnectionPool(host='i4.minus.com', port=80): Max retries exceeded 
                else:
                    print target_page.url
                    pin.true_source_url = target_page.url
                    pin.save()
                    print pin.id
                    print pin.true_source_url

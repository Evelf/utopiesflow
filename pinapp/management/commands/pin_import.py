# coding: utf-8
import requests
import json
from os.path import splitext
from datetime import datetime

from django.conf import settings
from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone
from django.utils.http import urlencode

from pinapp.models import Board, Pin


class Command(BaseCommand):
    # todo: https://github.com/joestump/python-oauth2/wiki/Signing-A-Request
    help = 'Import pins from Pinterest'

    @classmethod
    def get_url(cls):
        params = {
            'access_token': settings.PINAPP_ACCESS_TOKEN,
            'limit': 10,
            'fields': 'id,created_at,url,link,note,image,color,board',
        }
        return "%s%s?%s" % (settings.PINAPP_BASE_URL, 'pins/', urlencode(params))

    def handle(self, *args, **options):
        res = requests.get(self.get_url())
        if res.status_code != 200:
            self.stdout.write("%s: %s" % ('KO', res.status_code))
        else:
            data = json.loads(res.content)['data']
            page = json.loads(res.content)['page']
            for pin_data in data:
                board_defaults = {
                    'name': pin_data['board']['name'],
                }
                board, created = Board.objects.get_or_create(
                    board_id=pin_data['board']['id'],
                    defaults=board_defaults)
                if not created:
                    board.__dict__.update(board_defaults)
                    board.save()

                pin_date = datetime.strptime(
                    pin_data['created_at'],
                    '%Y-%m-%dT%H:%M:%S')
                pin_defaults = {
                    'created_at': pin_date.replace(tzinfo=timezone.utc),
                    'pin_url': pin_data['url'],
                    'source_url': pin_data['link'],
                    'note': pin_data['note'],
                    'source_url': pin_data['link'],
                    'image': '',
                    'color': pin_data['color'],
                    'board': board,
                }
                pin, created = Pin.objects.get_or_create(
                    pin_id=pin_data['id'], defaults=pin_defaults)
                if not created:
                    pin_defaults.pop('image')
                    pin.__dict__.update(pin_defaults)
                    pin.save()
                else:
                    res_img = requests.get(pin_data['image']['original']['url'])
                    ext = splitext(pin_data['image']['original']['url'])[1]
                    img_name = "%s%s" % (pin_data['id'], ext)
                    pin.image.save(img_name, ContentFile(res_img.content))
      #      self.stdout.write(res.content)

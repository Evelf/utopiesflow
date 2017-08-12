# coding: utf-8
import requests
from datetime import datetime
from os.path import splitext

from django.core.files.base import ContentFile
from django.utils import timezone

from pinapp.models import Board, Pin


class APITools(object):
    help = 'Tools for importing pins'

    @classmethod
    def api_fields(cls):
        fields = ['id', 'created_at', 'url', 'link', 'note', 'image',
                  'color', 'board', 'media', 'attribution',
                  'metadata', ]
        return ','.join(fields)

    @classmethod
    def update_pin(cls, pin_data, override_image=False):
        board_defaults = {
            'name': pin_data['board']['name'],
        }
        board, created = Board.objects.get_or_create(
            board_id=pin_data['board']['id'],
            defaults=board_defaults)
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
            'media_type': pin_data['media']['type'],
            'video_data': pin_data['attribution'] or {},
            'metadata': pin_data['metadata'] or {},
            'color': pin_data['color'],
            'board': board,
        }
        pin, created = Pin.objects.get_or_create(
            pin_id=pin_data['id'], defaults=pin_defaults)
        if not created:
            pin_defaults.pop('image')
            pin.__dict__.update(pin_defaults)
            pin.save()
        if created or override_image:
            image_url = pin_data['image']['original']['url']
            APITools.override_image(pin, image_url)

    @classmethod
    def override_image(cls, pin, image_url):
        res_img = requests.get(image_url)
        ext = splitext(image_url)[1]
        img_name = "%s%s" % (pin.pin_id, ext)
        pin.image.save(img_name, ContentFile(res_img.content))

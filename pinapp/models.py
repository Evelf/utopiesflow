# coding: utf-8
from __future__ import unicode_literals

from django.contrib.postgres.fields import JSONField
from django.db import models
from django.utils.encoding import python_2_unicode_compatible


@python_2_unicode_compatible  # only if you need to support Python 2
class Pin(models.Model):
    pin_id = models.CharField(  # API field: id
        max_length=50,
        help_text='The unique string of numbers and letters that identifies'
                  ' the Pin on Pinterest.')
    created_at = models.DateTimeField(  # API field: created_at
        'created at', help_text='The date the Pin was created.')
    # TODO: make an other table for urls.
    pin_url = models.CharField(  # API field: url
        max_length=250,
        help_text='The URL of the Pin on Pinterest. Should be more than 2000'
                  ' to be sure.')
    # TODO: make an other table for urls.
    source_url = models.CharField(  # API field: link
        max_length=250,
        help_text='The URL of the webpage where the Pin was'
                  ' created. Should be more than 2000 to be sure.')
    note = models.TextField(  # API field: note
        default='',
        help_text='The user-entered description of the Pin.')
    image = models.ImageField(  # API field: image
        upload_to='pinpics', height_field=None, width_field=None,
        max_length=100,
        help_text='The Pin’s image. The default response returns the image’s'
                  ' URL, width and height.'
    )
    color = models.CharField(  # API field: color
        max_length=7,
        help_text='The dominant color of the'
                  ' Pin’s image in hex code format.')
    board = models.ForeignKey(  # API field: board
        'Board', models.SET_NULL, blank=True, null=True,
        help_text='The board that the Pin is on.',
    )
    media_type = models.CharField(  # API field: media
        max_length=5,
        help_text='The media type of the Pin (image or video).',
    )
    video_data = JSONField(  # API field: attribution
        default={},
        help_text='The source data for videos, including the title, URL,'
                  ' provider, author name, author URL and provider name.',
    )
    metadata = JSONField(  # API field: metadat
        default={},
        help_text='Extra information about the Pin for Rich Pins. Includes the'
                  ' Pin type (e.g., article, recipe) and related information'
                  ' (e.g., ingredients, author).'
    )
    # creator map<string,string> The first and last name, ID and profile URL
    #   of the user who created the board.
    # counts map<string,i32>     The Pin’s stats, including the number of
    #   repins, comments and likes.

    def __str__(self):
        return self.pin_id


@python_2_unicode_compatible  # only if you need to support Python 2
class Board(models.Model):
    board_id = models.CharField(  # API field: id
        max_length=50,
        help_text='The unique string of numbers and letters that identifies'
                  ' the board on Pinterest.')
    name = models.CharField(  # API field: name
        max_length=50, help_text='The name of the board.')
    created_at = models.DateTimeField(  # API field: created_at
        'created at', auto_now_add=True,
        help_text='The date the user created the board.')
    # url string The link to the board.
    # description string The user-entered description of the board.
    # creator map<string,string> The first and last name, ID and profile URL
    #   of the user who created the board.
    # counts map<string,i32> The board’s stats, including how many Pins,
    #   followers, user's following and collaborators it has.
    # image map<string,image> The user’s profile image. The response returns
    #   the image’s URL, width and height.

    def __str__(self):
        return self.name

# coding: utf-8
import json
import os.path

from django.core.management import call_command
from django.test import TestCase

import responses
from pinapp.management.commands.pin_import import Command as PinImportCommand
from pinapp.models import Board, Pin


class TestCommands(TestCase):

    def setUp(self):
        mock_filename = os.path.join(os.path.dirname(__file__), 'api.mock')
        with open(mock_filename) as f:
            body = f.read()
        responses.add(
            responses.GET, PinImportCommand.get_url(),
            match_querystring=True,
            body=body, content_type="application/json")

        data = json.loads(body)['data']
        mock_image_filename = os.path.join(
            os.path.dirname(__file__), 'fee.png'
        )
        with open(mock_image_filename) as f:
            image = f.read()
        for pin_data in data:
            responses.add(
                responses.GET, pin_data['image']['original']['url'],
                body=image)

    @responses.activate
    def test_import(self):
        call_command('pin_import')

        assert len(responses.calls) == 11
        assert responses.calls[0].request.url == PinImportCommand.get_url()

        assert Pin.objects.count() == 10
        assert Board.objects.count() == 4

    @responses.activate
    def test_import_update(self):
        call_command('pin_import')
        call_command('pin_import')

        assert len(responses.calls) == 12
        assert responses.calls[0].request.url == PinImportCommand.get_url()
        assert responses.calls[11].request.url == PinImportCommand.get_url()

        assert Pin.objects.count() == 10
        assert Board.objects.count() == 4

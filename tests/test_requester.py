from __future__ import absolute_import, division, print_function, unicode_literals
import unittest

import requests_mock

from canvasapi import Canvas
from canvasapi.exceptions import (
    BadRequest, CanvasException, InvalidAccessToken, ResourceDoesNotExist,
    Unauthorized
)
from tests import settings
from tests.util import register_uris


@requests_mock.Mocker()
class TestRequester(unittest.TestCase):

    def setUp(self):
        self.canvas = Canvas(settings.BASE_URL, settings.API_KEY)
        self.requester = self.canvas._Canvas__requester

    # request()
    def test_request_get(self, m):
        register_uris({'requests': ['get']}, m)

        response = self.requester.request('GET', 'fake_get_request')
        self.assertEqual(response.status_code, 200)

    def test_request_post(self, m):
        register_uris({'requests': ['post']}, m)

        response = self.requester.request('POST', 'fake_post_request')
        self.assertEqual(response.status_code, 200)

    def test_request_delete(self, m):
        register_uris({'requests': ['delete']}, m)

        response = self.requester.request('DELETE', 'fake_delete_request')
        self.assertEqual(response.status_code, 200)

    def test_request_put(self, m):
        register_uris({'requests': ['put']}, m)

        response = self.requester.request('PUT', 'fake_put_request')
        self.assertEqual(response.status_code, 200)

    def test_request_400(self, m):
        register_uris({'requests': ['400']}, m)

        with self.assertRaises(BadRequest):
            self.requester.request('GET', '400')

    def test_request_401_InvalidAccessToken(self, m):
        register_uris({'requests': ['401_invalid_access_token']}, m)

        with self.assertRaises(InvalidAccessToken):
            self.requester.request('GET', '401_invalid_access_token')

    def test_request_401_Unauthorized(self, m):
        register_uris({'requests': ['401_unauthorized']}, m)

        with self.assertRaises(Unauthorized):
            self.requester.request('GET', '401_unauthorized')

    def test_request_404(self, m):
        register_uris({'requests': ['404']}, m)

        with self.assertRaises(ResourceDoesNotExist):
            self.requester.request('GET', '404')

    def test_request_500(self, m):
        register_uris({'requests': ['500']}, m)

        with self.assertRaises(CanvasException):
            self.requester.request('GET', '500')

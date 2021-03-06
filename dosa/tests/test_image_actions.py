import json
import os.path
from unittest import TestCase
from unittest.mock import patch

import dosa

endpoint = 'https://api.digitalocean.com/%s' % dosa.API_VERSION
api_sample_data = os.path.join(os.path.dirname(__file__), 'api_sample_data')

class TestDosaClientDropletActions(TestCase):
    @classmethod
    def setUp(self):
        self.api_key = 'my_fake_api_key'
        self.client = dosa.Client(self.api_key)

    @classmethod
    def tearDown(self):
        pass

    def test_dosa_client_created(self):
        client = dosa.Client(self.api_key)
        self.assertIsInstance(client, dosa.Client)

    @patch('dosa.requests.get')
    def test_dosa_image_list(self, mock_get):
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = json.loads(self._get_sample_data('images'))
        status, result = self.client.images.list()
        self.assertEqual(1, len(result['images']))
        self.assertTrue(mock_get.called)

        expected_headers = {
            'Content-Type': 'application/json',
            'authorization': 'Bearer {}'.format(self.api_key)
        }
        expected_params = {}
        expected_data = '{}'
        url, data = mock_get.call_args
        self.assertEqual(url[0], '{}/images'.format(endpoint))
        self.assertDictEqual(data['headers'], expected_headers)
        self.assertDictEqual(data['params'], expected_params)
        self.assertEqual(data['data'], expected_data)


    @patch('dosa.requests.get')
    def test_dosa_image_by_search(self, mock_get):
        # TODO: Update library and test
        # Currently failing due to dosa/__init__.py L159 attempting to use name 'images' from response with 'image' key
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = json.loads(self._get_sample_data('images_search'))
        data_sample = json.loads(self._get_sample_data('images_search'))
        image_slug = data_sample['image']['slug']
        image = self.client.images.search('ubuntu')
        status, image_info = image.info()
        self.assertTrue(mock_get.called)
        expected_headers = {
            'Content-Type': 'application/json',
            'authorization': 'Bearer {}'.format(self.api_key)
        }
        expected_params = {}
        expected_data = '{}'
        url, data = mock_get.call_args
        self.assertEqual(url[0], '{}/images/{}'.format(endpoint, image_id))
        self.assertDictEqual(data['headers'], expected_headers)
        self.assertDictEqual(data['params'], expected_params)
        self.assertEqual(data['data'], expected_data)

    def _get_sample_data(self, path=''):
        return open(os.path.join(api_sample_data, '{}.json'.format(path))).read()

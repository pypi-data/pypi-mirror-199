"""
    SoftLayer.tests.CLI.modules.cdn_tests
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    :license: MIT, see LICENSE for more details.
"""
import datetime
import json
from unittest import mock as mock

from SoftLayer.CLI import exceptions
from SoftLayer import testing


class CdnTests(testing.TestCase):

    def test_list_accounts(self):
        result = self.run_command(['cdn', 'list'])

        self.assert_no_fail(result)
        self.assertEqual(json.loads(result.output),
                         [{'cname': 'cdnakauuiet7s6u6.cdnedge.bluemix.net',
                           'domain': 'test.example.com',
                           'origin': '1.1.1.1',
                           'status': 'CNAME_CONFIGURATION',
                           'unique_id': '11223344',
                           'vendor': 'akamai'}]
                         )

    @mock.patch('SoftLayer.utils.days_to_datetime')
    def test_detail_account(self, mock_now):
        mock_now.return_value = datetime.datetime(2020, 1, 1)
        result = self.run_command(['cdn', 'detail', '--history=30', '1245'])

        self.assert_no_fail(result)
        api_results = json.loads(result.output)
        self.assertEqual(api_results['hit_ratio'], '2.0 %')
        self.assertEqual(api_results['total_bandwidth'], '1.0 GB')
        self.assertEqual(api_results['total_hits'], 3)
        self.assertEqual(api_results['hostname'], 'test.example.com')
        self.assertEqual(api_results['protocol'], 'HTTP')

    def test_purge_content(self):
        result = self.run_command(['cdn', 'purge', '1234',
                                   '/article/file.txt'])

        self.assert_no_fail(result)

    def test_list_origins(self):
        result = self.run_command(['cdn', 'origin-list', '1234'])

        self.assert_no_fail(result)
        self.assertEqual(json.loads(result.output), [{'HTTP Port': 80,
                                                      'Origin': '10.10.10.1',
                                                      'Path': '/example',
                                                      'Status': 'RUNNING'},
                                                     {'HTTP Port': 80,
                                                      'Origin': '10.10.10.1',
                                                      'Path': '/example1',
                                                      'Status': 'RUNNING'}])

    def test_add_origin_server(self):
        result = self.run_command(
            ['cdn', 'origin-add', '-t', 'server', '-H=test.example.com', '-p', 80, '-o', 'web', '-c=include-all',
             '1234', '10.10.10.1', '/example/videos2'])

        self.assert_no_fail(result)

    def test_add_origin_storage(self):
        result = self.run_command(['cdn', 'origin-add', '-t', 'storage', '-b=test-bucket', '-H=test.example.com',
                                   '-p', 80, '-o', 'web', '-c=include-all', '1234', '10.10.10.1', '/example/videos2'])

        self.assert_no_fail(result)

    def test_add_origin_without_storage(self):
        result = self.run_command(['cdn', 'origin-add', '-t', 'storage', '-H=test.example.com', '-p', 80,
                                   '-o', 'web', '-c=include-all', '1234', '10.10.10.1', '/example/videos2'])

        self.assertEqual(result.exit_code, 2)
        self.assertIsInstance(result.exception, exceptions.ArgumentError)

    def test_add_origin_storage_with_file_extensions(self):
        result = self.run_command(
            ['cdn', 'origin-add', '-t', 'storage', '-b=test-bucket', '-e', 'jpg', '-H=test.example.com', '-p', 80,
             '-o', 'web', '-c=include-all', '1234', '10.10.10.1', '/example/videos2'])

        self.assert_no_fail(result)

    def test_remove_origin(self):
        result = self.run_command(['cdn', 'origin-remove', '1234',
                                   '/example1'])

        self.assert_no_fail(result)
        self.assertEqual(result.output, "Origin with path /example1 has been deleted\n")

    def test_edit_header(self):
        result = self.run_command(['cdn', 'edit', 'test.example.com', '--header=www.test.com'])
        self.assert_no_fail(result)
        header_result = json.loads(result.output)
        self.assertEqual('www.test.com', header_result['Header'])

    def test_edit_http_port(self):
        result = self.run_command(['cdn', 'edit', 'test.example.com', '--http-port=83'])
        self.assert_no_fail(result)
        header_result = json.loads(result.output)
        self.assertEqual(83, header_result['Http Port'])

    def test_edit_respect_headers(self):
        result = self.run_command(['cdn', 'edit', 'test.example.com', '--respect-headers=1'])
        self.assert_no_fail(result)
        header_result = json.loads(result.output)
        self.assertEqual(True, header_result['Respect Headers'])

    def test_edit_cache(self):
        result = self.run_command(['cdn', 'edit', 'test.example.com', '--cache', 'include-specified',
                                   '--cache', 'test'])
        self.assert_no_fail(result)
        header_result = json.loads(result.output)
        self.assertEqual('include: test', header_result['Cache key optimization'])

    def test_edit_cache_by_uniqueId(self):
        result = self.run_command(['cdn', 'edit', '11223344', '--cache', 'include-specified', '--cache', 'test'])
        self.assert_no_fail(result)
        header_result = json.loads(result.output)
        self.assertEqual('include: test', header_result['Cache key optimization'])

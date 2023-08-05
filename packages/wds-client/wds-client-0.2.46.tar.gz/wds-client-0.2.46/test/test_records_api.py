# coding: utf-8

"""
    Workspace Data Service

    This page lists current APIs.  As of v0.2, all APIs are subject to change without notice.   # noqa: E501

    The version of the OpenAPI document: v0.2
    Generated by: https://openapi-generator.tech
"""


from __future__ import absolute_import

import unittest

import wds_client
from wds_client.api.records_api import RecordsApi  # noqa: E501
from wds_client.rest import ApiException


class TestRecordsApi(unittest.TestCase):
    """RecordsApi unit test stubs"""

    def setUp(self):
        self.api = wds_client.api.records_api.RecordsApi()  # noqa: E501

    def tearDown(self):
        pass

    def test_batch_write_records(self):
        """Test case for batch_write_records

        Batch write records  # noqa: E501
        """
        pass

    def test_create_or_replace_record(self):
        """Test case for create_or_replace_record

        Create or replace record  # noqa: E501
        """
        pass

    def test_delete_record(self):
        """Test case for delete_record

        Delete record  # noqa: E501
        """
        pass

    def test_get_record(self):
        """Test case for get_record

        Get record  # noqa: E501
        """
        pass

    def test_get_records_as_tsv(self):
        """Test case for get_records_as_tsv

        Retrieve all records in record type as tsv.  # noqa: E501
        """
        pass

    def test_query_records(self):
        """Test case for query_records

        Query records  # noqa: E501
        """
        pass

    def test_update_record(self):
        """Test case for update_record

        Update record  # noqa: E501
        """
        pass

    def test_upload_tsv(self):
        """Test case for upload_tsv

        Import records to a record type from a tsv file  # noqa: E501
        """
        pass


if __name__ == '__main__':
    unittest.main()

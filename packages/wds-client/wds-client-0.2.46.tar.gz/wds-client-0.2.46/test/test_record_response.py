# coding: utf-8

"""
    Workspace Data Service

    This page lists current APIs.  As of v0.2, all APIs are subject to change without notice.   # noqa: E501

    The version of the OpenAPI document: v0.2
    Generated by: https://openapi-generator.tech
"""


from __future__ import absolute_import

import unittest
import datetime

import wds_client
from wds_client.models.record_response import RecordResponse  # noqa: E501
from wds_client.rest import ApiException

class TestRecordResponse(unittest.TestCase):
    """RecordResponse unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional):
        """Test RecordResponse
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # model = wds_client.models.record_response.RecordResponse()  # noqa: E501
        if include_optional :
            return RecordResponse(
                id = '0', 
                type = '0', 
                attributes = {
  "stringAttr": "string",
  "numericAttr": 123,
  "booleanAttr": true,
  "relationAttr": "terra-wds:/target-type/target-id",
  "fileAttr": "https://account_name.blob.core.windows.net/container-1/blob1",
  "arrayString": ["green", "red"],
  "arrayBoolean": [true, false],
  "arrayNumber": [12821.112, 0.12121211, 11],
  "arrayDate": ["2022-11-03"],
  "arrayDateTime": ["2022-11-03T04:36:20"],
  "arrayRelation": ["terra-wds:/target-type/target-id-1", "terra-wds:/target-type/target-id-2"],
  "arrayFile": ["drs://drs.example.org/file_id_1", "https://account_name.blob.core.windows.net/container-2/blob2"]
}

            )
        else :
            return RecordResponse(
                id = '0',
                type = '0',
                attributes = {
  "stringAttr": "string",
  "numericAttr": 123,
  "booleanAttr": true,
  "relationAttr": "terra-wds:/target-type/target-id",
  "fileAttr": "https://account_name.blob.core.windows.net/container-1/blob1",
  "arrayString": ["green", "red"],
  "arrayBoolean": [true, false],
  "arrayNumber": [12821.112, 0.12121211, 11],
  "arrayDate": ["2022-11-03"],
  "arrayDateTime": ["2022-11-03T04:36:20"],
  "arrayRelation": ["terra-wds:/target-type/target-id-1", "terra-wds:/target-type/target-id-2"],
  "arrayFile": ["drs://drs.example.org/file_id_1", "https://account_name.blob.core.windows.net/container-2/blob2"]
}
,
        )

    def testRecordResponse(self):
        """Test RecordResponse"""
        inst_req_only = self.make_instance(include_optional=False)
        inst_req_and_optional = self.make_instance(include_optional=True)


if __name__ == '__main__':
    unittest.main()

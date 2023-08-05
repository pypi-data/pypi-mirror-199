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
from wds_client.models.inline_object import InlineObject  # noqa: E501
from wds_client.rest import ApiException

class TestInlineObject(unittest.TestCase):
    """InlineObject unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional):
        """Test InlineObject
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # model = wds_client.models.inline_object.InlineObject()  # noqa: E501
        if include_optional :
            return InlineObject(
                records = bytes(b'blah')
            )
        else :
            return InlineObject(
                records = bytes(b'blah'),
        )

    def testInlineObject(self):
        """Test InlineObject"""
        inst_req_only = self.make_instance(include_optional=False)
        inst_req_and_optional = self.make_instance(include_optional=True)


if __name__ == '__main__':
    unittest.main()

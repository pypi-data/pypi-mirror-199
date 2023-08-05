# coding: utf-8

"""
    Workspace Data Service

    This page lists current APIs.  As of v0.2, all APIs are subject to change without notice.   # noqa: E501

    The version of the OpenAPI document: v0.2
    Generated by: https://openapi-generator.tech
"""


from __future__ import absolute_import

import re  # noqa: F401

# python 2 and python 3 compatibility library
import six

from wds_client.api_client import ApiClient
from wds_client.exceptions import (  # noqa: F401
    ApiTypeError,
    ApiValueError
)


class InstancesApi(object):
    """NOTE: This class is auto generated by OpenAPI Generator
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """

    def __init__(self, api_client=None):
        if api_client is None:
            api_client = ApiClient()
        self.api_client = api_client

    def create_wds_instance(self, instanceid, v, **kwargs):  # noqa: E501
        """Create an instance  # noqa: E501

        Create an instance with the given UUID.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.create_wds_instance(instanceid, v, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str instanceid: WDS instance id; by convention equal to workspace id (required)
        :param str v: API version (required)
        :param str workspaceid: Id of workspace containing a WDS instance. If omitted, assumed to be equal to the instance id.
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: None
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        return self.create_wds_instance_with_http_info(instanceid, v, **kwargs)  # noqa: E501

    def create_wds_instance_with_http_info(self, instanceid, v, **kwargs):  # noqa: E501
        """Create an instance  # noqa: E501

        Create an instance with the given UUID.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.create_wds_instance_with_http_info(instanceid, v, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str instanceid: WDS instance id; by convention equal to workspace id (required)
        :param str v: API version (required)
        :param str workspaceid: Id of workspace containing a WDS instance. If omitted, assumed to be equal to the instance id.
        :param _return_http_data_only: response data without head status code
                                       and headers
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: None
                 If the method is called asynchronously,
                 returns the request thread.
        """

        local_var_params = locals()

        all_params = [
            'instanceid',
            'v',
            'workspaceid'
        ]
        all_params.extend(
            [
                'async_req',
                '_return_http_data_only',
                '_preload_content',
                '_request_timeout'
            ]
        )

        for key, val in six.iteritems(local_var_params['kwargs']):
            if key not in all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method create_wds_instance" % key
                )
            local_var_params[key] = val
        del local_var_params['kwargs']
        # verify the required parameter 'instanceid' is set
        if self.api_client.client_side_validation and ('instanceid' not in local_var_params or  # noqa: E501
                                                        local_var_params['instanceid'] is None):  # noqa: E501
            raise ApiValueError("Missing the required parameter `instanceid` when calling `create_wds_instance`")  # noqa: E501
        # verify the required parameter 'v' is set
        if self.api_client.client_side_validation and ('v' not in local_var_params or  # noqa: E501
                                                        local_var_params['v'] is None):  # noqa: E501
            raise ApiValueError("Missing the required parameter `v` when calling `create_wds_instance`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'instanceid' in local_var_params:
            path_params['instanceid'] = local_var_params['instanceid']  # noqa: E501
        if 'v' in local_var_params:
            path_params['v'] = local_var_params['v']  # noqa: E501

        query_params = []
        if 'workspaceid' in local_var_params and local_var_params['workspaceid'] is not None:  # noqa: E501
            query_params.append(('workspaceid', local_var_params['workspaceid']))  # noqa: E501

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['bearerAuth']  # noqa: E501

        return self.api_client.call_api(
            '/instances/{v}/{instanceid}', 'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type=None,  # noqa: E501
            auth_settings=auth_settings,
            async_req=local_var_params.get('async_req'),
            _return_http_data_only=local_var_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=local_var_params.get('_preload_content', True),
            _request_timeout=local_var_params.get('_request_timeout'),
            collection_formats=collection_formats)

    def delete_wds_instance(self, instanceid, v, **kwargs):  # noqa: E501
        """Delete an instance  # noqa: E501

        Delete the instance with the given UUID. This API is liable to change.  THIS WILL DELETE ALL DATA WITHIN THE INSTANCE. Be certain this is what you want to do.   # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.delete_wds_instance(instanceid, v, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str instanceid: WDS instance id; by convention equal to workspace id (required)
        :param str v: API version (required)
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: None
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        return self.delete_wds_instance_with_http_info(instanceid, v, **kwargs)  # noqa: E501

    def delete_wds_instance_with_http_info(self, instanceid, v, **kwargs):  # noqa: E501
        """Delete an instance  # noqa: E501

        Delete the instance with the given UUID. This API is liable to change.  THIS WILL DELETE ALL DATA WITHIN THE INSTANCE. Be certain this is what you want to do.   # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.delete_wds_instance_with_http_info(instanceid, v, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str instanceid: WDS instance id; by convention equal to workspace id (required)
        :param str v: API version (required)
        :param _return_http_data_only: response data without head status code
                                       and headers
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: None
                 If the method is called asynchronously,
                 returns the request thread.
        """

        local_var_params = locals()

        all_params = [
            'instanceid',
            'v'
        ]
        all_params.extend(
            [
                'async_req',
                '_return_http_data_only',
                '_preload_content',
                '_request_timeout'
            ]
        )

        for key, val in six.iteritems(local_var_params['kwargs']):
            if key not in all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method delete_wds_instance" % key
                )
            local_var_params[key] = val
        del local_var_params['kwargs']
        # verify the required parameter 'instanceid' is set
        if self.api_client.client_side_validation and ('instanceid' not in local_var_params or  # noqa: E501
                                                        local_var_params['instanceid'] is None):  # noqa: E501
            raise ApiValueError("Missing the required parameter `instanceid` when calling `delete_wds_instance`")  # noqa: E501
        # verify the required parameter 'v' is set
        if self.api_client.client_side_validation and ('v' not in local_var_params or  # noqa: E501
                                                        local_var_params['v'] is None):  # noqa: E501
            raise ApiValueError("Missing the required parameter `v` when calling `delete_wds_instance`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'instanceid' in local_var_params:
            path_params['instanceid'] = local_var_params['instanceid']  # noqa: E501
        if 'v' in local_var_params:
            path_params['v'] = local_var_params['v']  # noqa: E501

        query_params = []

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['bearerAuth']  # noqa: E501

        return self.api_client.call_api(
            '/instances/{v}/{instanceid}', 'DELETE',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type=None,  # noqa: E501
            auth_settings=auth_settings,
            async_req=local_var_params.get('async_req'),
            _return_http_data_only=local_var_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=local_var_params.get('_preload_content', True),
            _request_timeout=local_var_params.get('_request_timeout'),
            collection_formats=collection_formats)

    def list_wds_instances(self, v, **kwargs):  # noqa: E501
        """List instances  # noqa: E501

        List all instances in this server.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.list_wds_instances(v, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str v: API version (required)
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: list[str]
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        return self.list_wds_instances_with_http_info(v, **kwargs)  # noqa: E501

    def list_wds_instances_with_http_info(self, v, **kwargs):  # noqa: E501
        """List instances  # noqa: E501

        List all instances in this server.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.list_wds_instances_with_http_info(v, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str v: API version (required)
        :param _return_http_data_only: response data without head status code
                                       and headers
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: tuple(list[str], status_code(int), headers(HTTPHeaderDict))
                 If the method is called asynchronously,
                 returns the request thread.
        """

        local_var_params = locals()

        all_params = [
            'v'
        ]
        all_params.extend(
            [
                'async_req',
                '_return_http_data_only',
                '_preload_content',
                '_request_timeout'
            ]
        )

        for key, val in six.iteritems(local_var_params['kwargs']):
            if key not in all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method list_wds_instances" % key
                )
            local_var_params[key] = val
        del local_var_params['kwargs']
        # verify the required parameter 'v' is set
        if self.api_client.client_side_validation and ('v' not in local_var_params or  # noqa: E501
                                                        local_var_params['v'] is None):  # noqa: E501
            raise ApiValueError("Missing the required parameter `v` when calling `list_wds_instances`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'v' in local_var_params:
            path_params['v'] = local_var_params['v']  # noqa: E501

        query_params = []

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = []  # noqa: E501

        return self.api_client.call_api(
            '/instances/{v}', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='list[str]',  # noqa: E501
            auth_settings=auth_settings,
            async_req=local_var_params.get('async_req'),
            _return_http_data_only=local_var_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=local_var_params.get('_preload_content', True),
            _request_timeout=local_var_params.get('_request_timeout'),
            collection_formats=collection_formats)

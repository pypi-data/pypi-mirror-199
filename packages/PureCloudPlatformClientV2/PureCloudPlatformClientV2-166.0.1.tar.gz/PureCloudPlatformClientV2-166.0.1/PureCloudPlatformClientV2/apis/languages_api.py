# coding: utf-8

"""
LanguagesApi.py
Copyright 2016 SmartBear Software

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
"""

from __future__ import absolute_import

import sys
import os
import re

# python 2 and python 3 compatibility library
from six import iteritems

from ..configuration import Configuration
from ..api_client import ApiClient


class LanguagesApi(object):
    """
    NOTE: This class is auto generated by the swagger code generator program.
    Do not edit the class manually.
    Ref: https://github.com/swagger-api/swagger-codegen
    """

    def __init__(self, api_client=None):
        config = Configuration()
        if api_client:
            self.api_client = api_client
        else:
            if not config.api_client:
                config.api_client = ApiClient()
            self.api_client = config.api_client

    def delete_language(self, language_id, **kwargs):
        """
        Delete Language (Deprecated)
        This endpoint is deprecated. Please see the Routing API (DELETE /api/v2/routing/languages/{languageId})

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please define a `callback` function
        to be invoked when receiving the response.
        >>> def callback_function(response):
        >>>     pprint(response)
        >>>
        >>> thread = api.delete_language(language_id, callback=callback_function)

        :param callback function: The callback function
            for asynchronous request. (optional)
        :param str language_id: Language ID (required)
        :return: None
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['language_id']
        all_params.append('callback')

        params = locals()
        for key, val in iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method delete_language" % key
                )
            params[key] = val
        del params['kwargs']

        # verify the required parameter 'language_id' is set
        if ('language_id' not in params) or (params['language_id'] is None):
            raise ValueError("Missing the required parameter `language_id` when calling `delete_language`")


        resource_path = '/api/v2/languages/{languageId}'.replace('{format}', 'json')
        path_params = {}
        if 'language_id' in params:
            path_params['languageId'] = params['language_id']

        query_params = {}

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None

        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.\
            select_header_accept(['application/json'])
        if not header_params['Accept']:
            del header_params['Accept']

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.\
            select_header_content_type(['application/json'])

        # Authentication setting
        auth_settings = ['PureCloud OAuth']

        response = self.api_client.call_api(resource_path, 'DELETE',
                                            path_params,
                                            query_params,
                                            header_params,
                                            body=body_params,
                                            post_params=form_params,
                                            files=local_var_files,
                                            response_type=None,
                                            auth_settings=auth_settings,
                                            callback=params.get('callback'))
        return response

    def get_language(self, language_id, **kwargs):
        """
        Get Language (Deprecated)
        This endpoint is deprecated. Please see the Routing API (GET /api/v2/routing/languages/{languageId})

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please define a `callback` function
        to be invoked when receiving the response.
        >>> def callback_function(response):
        >>>     pprint(response)
        >>>
        >>> thread = api.get_language(language_id, callback=callback_function)

        :param callback function: The callback function
            for asynchronous request. (optional)
        :param str language_id: Language ID (required)
        :return: Language
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['language_id']
        all_params.append('callback')

        params = locals()
        for key, val in iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method get_language" % key
                )
            params[key] = val
        del params['kwargs']

        # verify the required parameter 'language_id' is set
        if ('language_id' not in params) or (params['language_id'] is None):
            raise ValueError("Missing the required parameter `language_id` when calling `get_language`")


        resource_path = '/api/v2/languages/{languageId}'.replace('{format}', 'json')
        path_params = {}
        if 'language_id' in params:
            path_params['languageId'] = params['language_id']

        query_params = {}

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None

        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.\
            select_header_accept(['application/json'])
        if not header_params['Accept']:
            del header_params['Accept']

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.\
            select_header_content_type(['application/json'])

        # Authentication setting
        auth_settings = ['PureCloud OAuth']

        response = self.api_client.call_api(resource_path, 'GET',
                                            path_params,
                                            query_params,
                                            header_params,
                                            body=body_params,
                                            post_params=form_params,
                                            files=local_var_files,
                                            response_type='Language',
                                            auth_settings=auth_settings,
                                            callback=params.get('callback'))
        return response

    def get_languages(self, **kwargs):
        """
        Get the list of supported languages. (Deprecated)
        This endpoint is deprecated. Please see the Routing API (GET /api/v2/routing/languages)

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please define a `callback` function
        to be invoked when receiving the response.
        >>> def callback_function(response):
        >>>     pprint(response)
        >>>
        >>> thread = api.get_languages(callback=callback_function)

        :param callback function: The callback function
            for asynchronous request. (optional)
        :param int page_size: Page size
        :param int page_number: Page number
        :param str sort_order: Ascending or descending sort order
        :param str name: Name
        :return: LanguageEntityListing
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['page_size', 'page_number', 'sort_order', 'name']
        all_params.append('callback')

        params = locals()
        for key, val in iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method get_languages" % key
                )
            params[key] = val
        del params['kwargs']



        resource_path = '/api/v2/languages'.replace('{format}', 'json')
        path_params = {}

        query_params = {}
        if 'page_size' in params:
            query_params['pageSize'] = params['page_size']
        if 'page_number' in params:
            query_params['pageNumber'] = params['page_number']
        if 'sort_order' in params:
            query_params['sortOrder'] = params['sort_order']
        if 'name' in params:
            query_params['name'] = params['name']

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None

        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.\
            select_header_accept(['application/json'])
        if not header_params['Accept']:
            del header_params['Accept']

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.\
            select_header_content_type(['application/json'])

        # Authentication setting
        auth_settings = ['PureCloud OAuth']

        response = self.api_client.call_api(resource_path, 'GET',
                                            path_params,
                                            query_params,
                                            header_params,
                                            body=body_params,
                                            post_params=form_params,
                                            files=local_var_files,
                                            response_type='LanguageEntityListing',
                                            auth_settings=auth_settings,
                                            callback=params.get('callback'))
        return response

    def get_languages_translations(self, **kwargs):
        """
        Get all available languages for translation
        

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please define a `callback` function
        to be invoked when receiving the response.
        >>> def callback_function(response):
        >>>     pprint(response)
        >>>
        >>> thread = api.get_languages_translations(callback=callback_function)

        :param callback function: The callback function
            for asynchronous request. (optional)
        :return: AvailableTranslations
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = []
        all_params.append('callback')

        params = locals()
        for key, val in iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method get_languages_translations" % key
                )
            params[key] = val
        del params['kwargs']



        resource_path = '/api/v2/languages/translations'.replace('{format}', 'json')
        path_params = {}

        query_params = {}

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None

        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.\
            select_header_accept(['application/json'])
        if not header_params['Accept']:
            del header_params['Accept']

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.\
            select_header_content_type(['application/json'])

        # Authentication setting
        auth_settings = ['PureCloud OAuth']

        response = self.api_client.call_api(resource_path, 'GET',
                                            path_params,
                                            query_params,
                                            header_params,
                                            body=body_params,
                                            post_params=form_params,
                                            files=local_var_files,
                                            response_type='AvailableTranslations',
                                            auth_settings=auth_settings,
                                            callback=params.get('callback'))
        return response

    def get_languages_translations_builtin(self, language, **kwargs):
        """
        Get the builtin translation for a language
        

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please define a `callback` function
        to be invoked when receiving the response.
        >>> def callback_function(response):
        >>>     pprint(response)
        >>>
        >>> thread = api.get_languages_translations_builtin(language, callback=callback_function)

        :param callback function: The callback function
            for asynchronous request. (optional)
        :param str language: The language of the builtin translation to retrieve (required)
        :return: dict(str, object)
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['language']
        all_params.append('callback')

        params = locals()
        for key, val in iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method get_languages_translations_builtin" % key
                )
            params[key] = val
        del params['kwargs']

        # verify the required parameter 'language' is set
        if ('language' not in params) or (params['language'] is None):
            raise ValueError("Missing the required parameter `language` when calling `get_languages_translations_builtin`")


        resource_path = '/api/v2/languages/translations/builtin'.replace('{format}', 'json')
        path_params = {}

        query_params = {}
        if 'language' in params:
            query_params['language'] = params['language']

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None

        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.\
            select_header_accept(['application/json'])
        if not header_params['Accept']:
            del header_params['Accept']

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.\
            select_header_content_type(['application/json'])

        # Authentication setting
        auth_settings = ['PureCloud OAuth']

        response = self.api_client.call_api(resource_path, 'GET',
                                            path_params,
                                            query_params,
                                            header_params,
                                            body=body_params,
                                            post_params=form_params,
                                            files=local_var_files,
                                            response_type='dict(str, object)',
                                            auth_settings=auth_settings,
                                            callback=params.get('callback'))
        return response

    def get_languages_translations_organization(self, language, **kwargs):
        """
        Get effective translation for an organization by language
        

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please define a `callback` function
        to be invoked when receiving the response.
        >>> def callback_function(response):
        >>>     pprint(response)
        >>>
        >>> thread = api.get_languages_translations_organization(language, callback=callback_function)

        :param callback function: The callback function
            for asynchronous request. (optional)
        :param str language: The language of the translation to retrieve for the organization (required)
        :return: dict(str, object)
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['language']
        all_params.append('callback')

        params = locals()
        for key, val in iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method get_languages_translations_organization" % key
                )
            params[key] = val
        del params['kwargs']

        # verify the required parameter 'language' is set
        if ('language' not in params) or (params['language'] is None):
            raise ValueError("Missing the required parameter `language` when calling `get_languages_translations_organization`")


        resource_path = '/api/v2/languages/translations/organization'.replace('{format}', 'json')
        path_params = {}

        query_params = {}
        if 'language' in params:
            query_params['language'] = params['language']

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None

        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.\
            select_header_accept(['application/json'])
        if not header_params['Accept']:
            del header_params['Accept']

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.\
            select_header_content_type(['application/json'])

        # Authentication setting
        auth_settings = ['PureCloud OAuth']

        response = self.api_client.call_api(resource_path, 'GET',
                                            path_params,
                                            query_params,
                                            header_params,
                                            body=body_params,
                                            post_params=form_params,
                                            files=local_var_files,
                                            response_type='dict(str, object)',
                                            auth_settings=auth_settings,
                                            callback=params.get('callback'))
        return response

    def get_languages_translations_user(self, user_id, **kwargs):
        """
        Get effective language translation for a user
        

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please define a `callback` function
        to be invoked when receiving the response.
        >>> def callback_function(response):
        >>>     pprint(response)
        >>>
        >>> thread = api.get_languages_translations_user(user_id, callback=callback_function)

        :param callback function: The callback function
            for asynchronous request. (optional)
        :param str user_id: The user id (required)
        :return: dict(str, object)
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['user_id']
        all_params.append('callback')

        params = locals()
        for key, val in iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method get_languages_translations_user" % key
                )
            params[key] = val
        del params['kwargs']

        # verify the required parameter 'user_id' is set
        if ('user_id' not in params) or (params['user_id'] is None):
            raise ValueError("Missing the required parameter `user_id` when calling `get_languages_translations_user`")


        resource_path = '/api/v2/languages/translations/users/{userId}'.replace('{format}', 'json')
        path_params = {}
        if 'user_id' in params:
            path_params['userId'] = params['user_id']

        query_params = {}

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None

        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.\
            select_header_accept(['application/json'])
        if not header_params['Accept']:
            del header_params['Accept']

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.\
            select_header_content_type(['application/json'])

        # Authentication setting
        auth_settings = ['PureCloud OAuth']

        response = self.api_client.call_api(resource_path, 'GET',
                                            path_params,
                                            query_params,
                                            header_params,
                                            body=body_params,
                                            post_params=form_params,
                                            files=local_var_files,
                                            response_type='dict(str, object)',
                                            auth_settings=auth_settings,
                                            callback=params.get('callback'))
        return response

    def post_languages(self, body, **kwargs):
        """
        Create Language (Deprecated)
        This endpoint is deprecated. Please see the Routing API. (POST /api/v2/routing/languages

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please define a `callback` function
        to be invoked when receiving the response.
        >>> def callback_function(response):
        >>>     pprint(response)
        >>>
        >>> thread = api.post_languages(body, callback=callback_function)

        :param callback function: The callback function
            for asynchronous request. (optional)
        :param Language body: Language (required)
        :return: Language
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['body']
        all_params.append('callback')

        params = locals()
        for key, val in iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method post_languages" % key
                )
            params[key] = val
        del params['kwargs']

        # verify the required parameter 'body' is set
        if ('body' not in params) or (params['body'] is None):
            raise ValueError("Missing the required parameter `body` when calling `post_languages`")


        resource_path = '/api/v2/languages'.replace('{format}', 'json')
        path_params = {}

        query_params = {}

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        if 'body' in params:
            body_params = params['body']

        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.\
            select_header_accept(['application/json'])
        if not header_params['Accept']:
            del header_params['Accept']

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.\
            select_header_content_type(['application/json'])

        # Authentication setting
        auth_settings = ['PureCloud OAuth']

        response = self.api_client.call_api(resource_path, 'POST',
                                            path_params,
                                            query_params,
                                            header_params,
                                            body=body_params,
                                            post_params=form_params,
                                            files=local_var_files,
                                            response_type='Language',
                                            auth_settings=auth_settings,
                                            callback=params.get('callback'))
        return response

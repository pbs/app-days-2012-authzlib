# -*- coding: utf-8 -*-
"""
    authzlib.auth
    ~~~~~~~~~~~~~

    Authz client implementation for the authentication and authorization
    services

    :copyright: (c) 2012 by Ion Scerbatiuc
    :license: BSD
"""
import urllib2
from urllib import quote_plus
try:
    import json
except ImportError:
    from simplejson import json

from authzlib.common import create_request, ensure_no_trailing_slash


class ObjectConfig(object):
    """Ensure that the configuration is an object."""

    def __new__(cls, config):
        if not isinstance(config, dict):
            return config

        return object.__new__(cls, config)

    def __init__(self, config):
        assert isinstance(config, dict)

        for key, value in config.iteritems():
            setattr(self, key, value)


class AuthClient(object):
    """Authz client implementation."""

    def __init__(self, config, config_prefix='AUTHZ_'):
        """Initialize and configure a new authz client object.

        Config should be an object that contains the necessary configuration
        options to communicate with the authz service:
          * ENDPOINT_URL - the URL to the authz service.
          * CLIENT_SERVICE - the service name to use when authorizing.
          * USER_AGENT (optional) - the user agent to use when sending requests
            Defaults to the urllib2 default user agent.

        By default the presented config options will be checked using the
        AUTHZ_ prefix (e.g. AUTHZ_ENDPOINT_URL). If can override this prefix
        by specifying the config_prefix argument.
        """
        config = ObjectConfig(config)

        self.endpoint_url = ensure_no_trailing_slash(
            getattr(config, '%sENDPOINT_URL' % config_prefix))
        self.service = getattr(config, '%sCLIENT_SERVICE' % config_prefix)
        self.user_agent = getattr(config, '%sUSER_AGENT' % config_prefix, None)

    def authenticate(self, method, url, body=None, headers=None):
        """Send an authentication request to the authz service.

        Returns the authenticated consumer as a dict or None if the
        authentication failed.
        """
        auth_url = "%s/authenticate/%s" % (self.endpoint_url, quote_plus(url, safe='/'))

        request = create_request(
            auth_url, method=method.upper(), body=body,
            user_agent=self.user_agent, headers=headers)

        try:
            response = urllib2.urlopen(request)
        except urllib2.HTTPError:
            return None
        else:
            return json.loads(response.read())

    def authorize(self, action, consumer_key, resource_id):
        """Send an authorization request to the authz service."""
        auth_url = "%s/authorize/%s/%s/%s/" % (
            self.endpoint_url, consumer_key, self.service, resource_id)

        request = create_request(
            auth_url, method=action.upper(),
            user_agent=self.user_agent)

        try:
            response = urllib2.urlopen(request)
        except urllib2.HTTPError:
            return False
        else:
            return response.code == 202

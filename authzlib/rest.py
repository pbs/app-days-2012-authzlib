# -*- coding: utf-8 -*-
"""
    authzlib.rest
    ~~~~~~~~~~~~

    Authz client implementation for the REST API

    :copyright: (c) 2012 by Edgar Roman
    :license: BSD
"""
import urllib2
try:
    import json
except ImportError:
    from simplejson import json

from authzlib.common import create_request, ensure_no_trailing_slash


class RestClient(object):
    """Authz REST API Lib implementation."""

    def __init__(self, base_url):
        """Initialize and configure a new authz rest object.
            Parameters:
                base_url - should point to the root of the Authz service
                    (e.g. http://api.pbs.org/authz/api/1.0)
        """
        self.base_url = ensure_no_trailing_slash(base_url)

    def get_consumer_list(self):
        """ Query the Authz API to return a list of Consumer objects
        """
        target_url = "%s/consumers/" % (self.base_url)
        request = create_request(target_url)
        try:
            response = urllib2.urlopen(request)
        except urllib2.HTTPError:
            return None

        raw_data = json.loads(response.read())
        consumers = []
        for rawc in raw_data['objects']:
            newc = Consumer(rawc['name'],
                            rawc['key'],
                            rawc['resource_uri'],
                            rawc['secret'],
                            rawc['policies'])
            consumers.append(newc)

        return consumers

    def add_consumer(self, new_consumer):
        """ Add a Authz consumer.
            The only required argument is consumer name
        """
        target_url = "%s/consumers/" % (self.base_url)
        post_body = json.dumps({ "name" : new_consumer.name })
        request = create_request(target_url,
                                  method="POST",
                                  body=post_body,
                                  content_type='application/json')
        try:
            response = urllib2.urlopen(request)
        except urllib2.HTTPError:
            return None

        rawc = json.loads(response.read())
        newc = Consumer(rawc['name'],
                        rawc['key'],
                        rawc['resource_uri'],
                        rawc['secret'],
                        rawc['policies'])

        return newc


class Consumer(object):
    """ Library representation of the Consumer object """
    def __init__(self, name, key=None, url=None, secret=None, policies=None):
        """Initialize and configure a new authz rest object.
            Parameters:
                base_url - should point to the root of the Authz service
                    (e.g. http://api.pbs.org/authz/api/1.0)
        """
        self.name = name
        if key:
            self.key = key
        if url:
            self.url = ensure_no_trailing_slash(url)
        if secret:
            self.secret = secret
        if policies:
            self.policies = ensure_no_trailing_slash(policies)

    def refresh_data(self, key):
        """ Get the latest data from the server -- generally shouldn't
        have to use this
        """
        pass

    def update_name(self, new_name):
        """ Function to update the name of the consumer
        """
        pass

    def delete(self):
        """ Remove this consumer from the system
        """
        pass

    def add_policy(self, Policy):
        """ Used to attach a policy to this consumer
        """
        pass

    def get_policy_list(self):
        """ Retrieve the list of policies attached to this consumer
        """
        pass

    def __unicode__(self):
        return self.name
    def __str__(self):
        return self.name


class Policy(object):
    """ Library representation of the Policy object """

    def __init__(self, rid, actions):
        """Initialize and configure a new authz rest object.
            Parameters:
                base_url - should point to the root of the Authz service
                    (e.g. http://api.pbs.org/authz/api/1.0)
        """
        self.rid = rid
        self.actions = actions

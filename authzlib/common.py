import urllib2


def create_request(url, method="GET", body=None, user_agent=None, headers=None):
    """Create a new urllib request with the specified HTTP method."""
    if not headers:
        request = urllib2.Request(url, data=body)
    else:
        request = urllib2.Request(url, data=body, headers=headers)

    request.get_method = lambda *a: method

    if user_agent:
        request.add_header('User-Agent', user_agent)

    return request


def ensure_no_trailing_slash(url):
    """Ensure that the specified URL does not ends with a slash."""
    if url.endswith('/'):
        return url[:-1]

    return url

import urllib2


def create_request(url,
                    method="GET",
                    body=None,
                    user_agent=None,
                    content_type=None):
    """Create a new urllib request with the specified HTTP method."""
    request = urllib2.Request(url, data=body)
    request.get_method = lambda *a: method

    if user_agent:
        request.add_header('User-Agent', user_agent)

    if body:
        request.add_header('Content-Length', len(body))
        if content_type:
            request.add_header('Content-Type', content_type)

    return request


def ensure_no_trailing_slash(url):
    """Ensure that the specified URL does not ends with a slash."""
    if url.endswith('/'):
        return url[:-1]

    return url

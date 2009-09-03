from django.shortcuts import render_to_response
from django.template import RequestContext

def render_response(req, *args, **kwargs):
    # This is bad.  You don't want to automagically inject request data into the response
    # since it can open an XSS or CSRF security hole.
    kwargs['context_instance'] = RequestContext(req)
    return render_to_response(*args, **kwargs)

import itertools
import logging

from django.utils.datastructures import MultiValueDict
from django.test.client import RequestFactory

def _get_page_key(path):
    if path == "/" or not path:
        page_key = "HOME"
    else:
        page_key = path.replace("/", "_").upper().strip("_")
    
    page_key = "PAGE_" + page_key
    return page_key

def generate_cache_key(request, get_args_to_consider=[]):
    path = request.path
    page_key = _get_page_key(path)
    
    param_parts = []
    for arg in sorted(get_args_to_consider):
        if arg in request.GET.keys():
            values = request.GET.getlist(arg)
            for value in values:
                param_parts.append("(%s,%s)" % (arg, value))
    
    if param_parts:
        param_part = "[%s]" % ",".join(param_parts)
        final_key = "%s-%s" % (page_key, param_part)
    else:
        final_key = page_key        
        
    return final_key

def get_possible_url_cache_keys(path, args=[]):
    """
        USAGE:
        keys = get_possible_url_cache_keys("/", [("page", 1), ("page", 2)])
    """
    
    #Generate all possible combinations of the args
    combination_set = set()
    args = sorted(args)
    for i in xrange(len(args)):
        combinations = itertools.combinations(args, i+1)
        for com in combinations:
            combination_set.add(com)
      
    page_key = _get_page_key(path) 
    urls = [ page_key ]
    for com in combination_set:
        param_parts = [ str(x).replace("'", "").replace(" ", "") for x in com ]
        param_part = "[%s]" % ",".join(param_parts)
        urls.append("%s-%s" % (page_key, param_part))
        
    return urls

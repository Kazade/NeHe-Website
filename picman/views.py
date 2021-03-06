from django.utils import simplejson
from django.shortcuts import render_to_response

def list_dir(path):
    sample = """[
    {
        "filename" : "file1.png",
        "type" : "file",
        "path" : "/some/download/file.png"
    },
    {
        "filename" : "folder1",
        "type" : "folder",
        "path" : "folder1"
    }
]"""

    return sample
    
def create_dir(request, path):
    pass
    
def upload_file(request, path):
    pass
    
def index(request):
    """
        The only view (really) in the picman app. This displays
        the folder listing, an upload input + button and an "up" button. The
        listing changes using Ajax.
        
        The Ajax listing is queried from the blobstore...
    """
    subs = {}
    subs["current_path"] = "/"
    subs["initial_files"] = simplejson.loads(list_dir(subs["current_path"]))
    return render_to_response("picman/index.html", subs)

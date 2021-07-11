import markdown
from django.shortcuts import render
from . import util



def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def wiki(request, title):
    entries = util.list_entries()
    if title in entries:
        page = util.get_entry(title)
        page_html = markdown.markdown(page)

        context = {
            'page': page_html,
            'title': title,
        }

        return render(request, "encyclopedia/wiki.html", context)
    else:
        return render(request, "encyclopedia/error.html", {"message": "the requested page does not exist." })


from django.shortcuts import render
from . import util
from django import forms
from markdown2 import Markdown
import random

converter = Markdown()

class New_Entry(forms.Form):
    title = forms.CharField(label= "Title")
    content = forms.CharField(widget=forms.Textarea(), label='content_area')

class Query(forms.Form):
    tag = forms.CharField(label='New Search')

class Edit(forms.Form):
    content = forms.CharField(widget=forms.Textarea(), label='content_area')


def edit(request, title):
    if request.method == 'GET':
        page = util.get_entry(title)
    
        body = {
            'form': Query(),
            'edit': Edit(initial={'content': page}),
            'title': title
        }
        return render(request, "encyclopedia/edit.html", body)
    else:
        form = Edit(request.POST)
        if form.is_valid():
            textarea = form.cleaned_data["content"]
            util.save_entry(title, textarea)
            page = util.get_entry(title)
            page_convert = converter.convert(page)
            
            body = {
                    'page': page_convert,
                    'title': title,
                    'form': Query(),
            }
            return render(request, "encyclopedia/entry.html", body)





def random_page(request):
    entries = util.list_entries()
    n = random.randint(0, len(entries)-1)
    title = entries[n]
    random_page = util.get_entry(title)
    page_convert = converter.convert(random_page)
    body = {
            'page': page_convert,
            'title': title,
            'form': Query()
        }
    return render(request, "encyclopedia/random.html", body)
    
def new_entry(request):
    if request.method =='POST':
        form = New_Entry(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]
            entries = util.list_entries()
            if title in entries:
                return render(request, "encyclopedia/error.html", {"form":Query(), "message":"Oopss. This page already exists!"} )
            else:
                util.save_entry(title, content)
                page = util.get_entry(title)
                page_convert = converter.convert(page)
                body = {
                    'page': page_convert,
                    'title': title,
                    'form': Query(),
                }

            return render(request, "encyclopedia/entry.html", body)

    return render(request, "encyclopedia/new.html", {"form": Query(), "post": New_Entry()})

def index(request):
    entries = util.list_entries()
    query = []
    if request.method == "POST":
        form = Query(request.POST)
        if form.is_valid():
            tag = form.cleaned_data["tag"]
            for i in entries:
                if tag in entries:
                    page = util.get_entry(tag)
                    page_converted = converter.convert(page)
                    
                    body = {
                        'page': page_converted,
                        'title': tag,
                        'form': Query()
                    }

                    return render(request, "encyclopedia/entry.html", body)

                if tag.lower() in i.lower():
                    query.append(i)
                    body = {
                        'searched': query, 
                        'form': Query()
                    }
                    return render(request, "encyclopedia/search.html", body)
                
            return render(request, "encyclopedia/error.html", {"form": Query(), "message": "The requested could not be found :(." })

        else:
            return render(request, "encyclopedia/wiki.html", {"form": form})
    else:
        return render(request, "encyclopedia/index.html", {
            "entries": util.list_entries(), "form":Query()
        })



def wiki(request, title):
    entries = util.list_entries()
    
    if title in entries:
        page = util.get_entry(title)
        page_convert = converter.convert(page)

        body = {
            'page': page_convert,
            'title': title,
            'form': Query(),
            'message':'it works'
        }
        return render(request, "encyclopedia/wiki.html", body)
    
    else:
        return render(request, "encyclopedia/error.html", {"form": Query(), "message": "The page requested could not be found :(" })




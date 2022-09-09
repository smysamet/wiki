from django.http import HttpResponseRedirect
from django.urls import reverse
from random import random
from django.shortcuts import render
from markdown2 import Markdown
from django.contrib import messages
from django.shortcuts import redirect
from . import util
import random

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        "index_heading":"All Pages"
    })


def wiki(request, title):
    content = mdToHtml(title)
    if content:
        return render(request, "encyclopedia/entry.html", {
            "title":title,
            "content":content
        })
    else:
        return render(request, "encyclopedia/404error.html", {
            "title":title
        })

def search(request):
    if request.method == "POST":
        q = request.POST["q"]

        content = mdToHtml(q)
        if content:
            return render(request, "encyclopedia/entry.html", {
                "title":q,
                "content":content
            })
        else:
            possible_list = []
            for entry in util.list_entries():
                # if q is a substring of the entry, add it to the possible list
                if q in entry:
                    possible_list.append(entry)
            
            return render(request, "encyclopedia/index.html", {
                "index_heading":"",
                "entries":possible_list
            })

def randomPage(request):
    # choose a random entry from all the entries
    entry = random.choice(util.list_entries())
    return render(request, "encyclopedia/entry.html", {
        "title": entry,
        "content":mdToHtml(entry)
    })

def newPage(request):

    if request.method == "POST":
        # get the contents of the POST method
        title = request.POST["title"]
        content = request.POST["content"]

        # server side verification 
        if title == "" or title is None:
            messages.error(request, f"Please add a title.")
            return HttpResponseRedirect(reverse("new-page"))

        if content == "" or content is None:
            messages.error(request, f"Please add a content.")
            return HttpResponseRedirect(reverse("new-page"))

        # check if the new added entry is already exist in the entries.
        if title in util.list_entries():
            messages.error(request, f"The {title} page already exists.")
            return HttpResponseRedirect(reverse("new-page"))

        util.save_entry(title, content)

        return render(request, "encyclopedia/entry.html", {
            "title":title,
            "content":mdToHtml(title)
        })
    return render(request, "encyclopedia/new-page.html")

def editEntry(request, title):

    if request.method == "POST":
        # get the contents of the POST method
        content = request.POST["content"]


        # server side verification
        if content == "" or content is None:
            messages.error(request, f"Content can not be empty!")
            return render(request, "encyclopedia/edit-entry.html", {
                "title":title,
                "content":util.get_entry(title)
            })
        
        util.save_entry(title, content)
        return redirect("wiki", title=title)

    return render(request, "encyclopedia/edit-entry.html", {
        "title":title,
        "content":util.get_entry(title)
    })



def mdToHtml(title):
    """Checks for the specific file with title (case sensitive), if founds a file it returns
    pure html, if it couldn't it returns None."""
    entry = util.get_entry(title)

    if entry:
        md = Markdown()
        pageAsHTML = md.convert(entry)
        return pageAsHTML
    else:
        return None
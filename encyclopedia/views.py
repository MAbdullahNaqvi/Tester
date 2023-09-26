from django.shortcuts import render,redirect
from django import forms
import markdown2
from random import choice

from . import util


class add_entry_form(forms.Form):
    title = forms.CharField(widget=forms.TextInput(attrs= {"class":"title", 'id':'title'}) ,label="Title")
    entry = forms.CharField(widget=forms.Textarea(attrs= {"class":"editor", 'id':'editor_add'}), label="Entry" )

class edit_entry_form(forms.Form):
    title = forms.CharField(widget=forms.HiddenInput(attrs= {"class":"edit_title", 'id':'title'}))
    entry = forms.CharField(widget=forms.Textarea(attrs= {"class":"editor", 'id':'editor_add'}), label="Entry" )

def index(request):
    
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
        
    })


def entry(request, entry):
    content = util.get_entry(entry)
    if not content:
        return render(request , "encyclopedia/error.html",{
            "Error" : "Requested Page not found"
        })
    converted = markdown2.markdown(content)
    
    return render(request, "encyclopedia/entry.html", {
        "content" : converted,
        "name" : entry
    })


def search(request):
    form = request.GET
    
    if not form:
        return redirect("/")
    
    if form.get("q") == "":
        return redirect("/")
    
    req_entry = form.get("q")
    entries_list = util.list_entries()
    if req_entry in entries_list:
        return redirect(f"/wiki/{req_entry}")
    entries = []
    for entry in entries_list:
        if req_entry in entry:
            entries += [entry]
    return render(request, "encyclopedia/search.html", {
        "search": req_entry,
        "entries" : entries,
        "length" : len(entries)
    })


def add_entry(request):
    
    if request.method == "POST":
        form = add_entry_form(request.POST)

        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["entry"]
            
            if  title in util.list_entries():
                
                form.add_error("title", "Title already in use chose another one")
                return render(request, "encyclopedia/add_entry.html", {
                "form": form
                })
            else:
                util.save_entry(title,content)
                return redirect("/")
            
        

    return render(request, "encyclopedia/add_entry.html", {
        "form": add_entry_form()
    })


def edit_entry(request):
    if request.method == "POST":
        form = edit_entry_form(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["entry"]
            util.save_entry(title,content)
            return redirect(f"/wiki/{title}")
            
        return
    else:
        get = request.GET
        if not get["title"]:
            return redirect("/")
        content = util.get_entry( get["title"])
        form = edit_entry_form({"title": get["title"], "entry": content})
        return render(request, "encyclopedia/edit_entry.html", {
            "form": form
        })


def random(request):
    entries = util.list_entries()
    random = choice(entries)
    print(random)
    return redirect(f"/wiki/{random}")
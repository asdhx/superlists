from django.shortcuts import render, redirect
from django.http import HttpResponse
from lists.models import Item, List
from lists.forms import ItemForm, ExistingListItemForm
from django.core.exceptions import ValidationError
from django.utils.html import escape


def home_page(request):
    return render(request, 'home.html', {'form': ItemForm()})

def view_list(request, list_id):
    list_ = List.objects.get(id=list_id)
    form = ExistingListItemForm(for_list = list_)
    if request.method == 'POST':
        form = ExistingListItemForm(for_list=list_, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect(list_)
            # return render(request, 'list.html', {'list': list_, "form": form, "error": error})
    return render(request, 'list.html', {'list': list_, "form": form})

def new_list(request):
    list_ = List.objects.create()
    form = ExistingListItemForm(for_list=list_, data=request.POST)
    if form.is_valid():
        form.save()
        return redirect(list_)
    return render(request, 'home.html', {"form": form})

from django.shortcuts import render, redirect

from datetime import datetime
from time import mktime

from django.http import JsonResponse, HttpResponse

from django.contrib import messages

import feedparser as fp

from .forms import UploadFileForm, RssStoreForm

from .models import RssStore, Entry, Searches, PatientNotes

import re


# def get_patient_notes(request, id):
#     pn = PatientNotes.objects.all()
#     context ={
#         'pn_history': pn.pn_history
#     }
#     return render(request, 'new.html', context)

# def single_rss(request, id):
#     my_rss = RssStore.objects.get(id=id)
#     entries = Entry.objects.filter(rss=my_rss)

#     # qs_json = serializers.serialize('json', entries)
#     context = {
#         'rss': my_rss,
#         'entries': entries,
#         'all': all_rss,
#     }
#     return render(request, 'single.html', context)

def single_rss(request, id):
    my_rss = RssStore.objects.get(id=id)
    pn = PatientNotes.objects.all()
    entries = Entry.objects.filter(rss=my_rss)
    

    # qs_json = serializers.serialize('json', entries)
    context = {
        'rss': my_rss,
        'entries': entries,
        'all': all_rss,
    }
    return render(request, 'single.html', context)





def all_rss(request):
    all = RssStore.objects.all()
    context = {
        'all': all,
    }
    return render(request, 'all.html', context)


def delete_rss(request, id):
    rss = RssStore.objects.get(id=id)
    rss.delete()
    return redirect('all')



def index(request):

    if request.method == "POST":
        form = RssStoreForm(request.POST, request.FILES)
        print(request.POST)
        if form.is_valid():
            # print(form.cleaned_data)
            form.save()
            messages.add_message(request, messages.SUCCESS, 'RSS Feed Saved Successfully. Go to All RSS to view feed.')
            return redirect('index')
    else:
        form = RssStoreForm()
    
    return render(request, 'index.html', {'form': form})


def basicdash(request): 

    totalGraphCount = 50
    numOfSavedCharts = 2

    context = {
        "numOfGraphs" : [49,50],  ##graphs that are loaded automatically once basicdash opens
        "newChartCount" : 1,
        "maxNewChart" : [totalGraphCount+1,totalGraphCount+2,totalGraphCount+3,totalGraphCount+4,totalGraphCount+5,totalGraphCount+6,totalGraphCount+7,totalGraphCount+8,totalGraphCount+9,totalGraphCount+10],  #total number of new graphs that can be added at a time
        "totalGraphCount": totalGraphCount,
    }

    return render(request, 'basicdash.html', context)

def basicdash2(request): 

    context = {'test' :1}

    return render(request, 'basicdash2.html', context)

def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            handle_uploaded_file(request.FILES['file'])
            # return HttpResponseRedirect('/success/url/')
    else:
        form = UploadFileForm()
    return render(request, 'upload.html', {'form': form})



    # if request.method == 'POST':
    #     form = UploadFileForm(request.POST, request.FILES)
    #     if form.is_valid():
    #         handle_uploaded_file(request.FILES['file'])
    #         print('noice')
    #         # return HttpResponseRedirect('/success/url/')
    # else:
    #     form = UploadFileForm()
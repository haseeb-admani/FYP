from django.shortcuts import render

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from reports.models import PatientNotes

import pandas as pd

# from django.db.models import Q


@api_view(['GET'])
def search_records(request):
    # search_query =
    # print(request.query_params)
    my_q = request.query_params['query']
    my_notes = PatientNotes.objects.values('id', 'record_date', 'history')
    my_notes = my_notes.filter(
        history__icontains=my_q)
    # print(len(my_notes))
    # print(my_q)
    if len(my_notes) > 0:
        # print(my_notes)
        notes = list(my_notes)
        # print(notes)
        df = pd.DataFrame(notes)
        df.record_date = pd.to_datetime(df.record_date)
        dg = df.groupby(pd.Grouper(key='record_date', freq='M')).count()
        dg.index = dg.index.strftime('%B')
        diag_monthly = dg.to_dict()
        diag_monthly = diag_monthly['id']
        # print(diag_monthly)
        months = ['January', 'February', 'March', 'April', 'May', 'June',
                  'July', 'August', 'September', 'October', 'November', 'December']
        diag_per_month = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        for my_key in diag_monthly.keys():
            index_of_month = months.index(my_key)
            diag_per_month[index_of_month] = diag_monthly[my_key]
        my_chart = {
            'label': months,
            'data': diag_per_month
        }
        # print(months)
        # print(diag_per_month)
    else:
        months = ['January', 'February', 'March', 'April', 'May', 'June',
                  'July', 'August', 'September', 'October', 'November', 'December']
        diag_per_month = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        my_chart = {
            'label': months,
            'data': diag_per_month
        }
    return Response(my_chart)
    # return Response("knock knock")


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

@api_view(['GET'])
def filtered_patients_data(request):
    filter_by = list(request.query_params.dict().values())
    my_notes = PatientNotes.objects.values('id', 'record_date', 'history')
    for my_filter in (filter_by):
        my_notes = my_notes.filter(history__icontains=my_filter)
    if len(my_notes) > 0:
        # print(my_notes)
        notes = list(my_notes)
        # print(notes)
        df = pd.DataFrame(notes)
        df.record_date = pd.to_datetime(df.record_date)
        dg = df.groupby(pd.Grouper(key='record_date', freq='M')).count()
        dg.index = dg.index.strftime('%B')
        diag_monthly = dg.to_dict()
        diag_monthly = diag_monthly['id']
        # print(diag_monthly)
        months = ['January', 'February', 'March', 'April', 'May', 'June',
                  'July', 'August', 'September', 'October', 'November', 'December']
        diag_per_month = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        for my_key in diag_monthly.keys():
            index_of_month = months.index(my_key)
            diag_per_month[index_of_month] = diag_monthly[my_key]
        my_chart = {
            'label': months,
            'data': diag_per_month
        }
        # print(months)
        # print(diag_per_month)
    else:
        months = ['January', 'February', 'March', 'April', 'May', 'June',
                  'July', 'August', 'September', 'October', 'November', 'December']
        diag_per_month = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        my_chart = {
            'label': months,
            'data': diag_per_month
        }
    return Response(my_chart)

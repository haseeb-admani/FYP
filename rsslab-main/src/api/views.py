from django.shortcuts import render

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from reports.models import PatientNotes
from datetime import datetime

import pandas as pd

# from django.db.models import Q


@api_view(['GET'])
def search_records(request):
    # search_query =
    # print(request.query_params)
    print("query params=  ", request.query_params)
    my_q = request.query_params['query']
    
    startDate = request.query_params['startDate']
    endDate = request.query_params['endDate']

    if(startDate != "" and endDate != ""):
        # startDate = datetime.strptime(startDate, "%Y-%m-%d").strftime('%Y-%m-%d')
        print("UPDATED DATE FILTER ", startDate)
        # endDate = datetime.strptime(endDate, "%Y-%m-%d").strftime('%Y-%m-%d')
        # query = query + " where record_date >= '{0}' and record_date <= '{1}'".format(startDate, endDate)
        my_notes = PatientNotes.objects.raw("select id, count(record_date) as month_count, substr(record_date, 6 , 2) as month from reports_patientnotes where history like '%{0}%' and record_date >= '{1}' and record_date <= '{2}' group by substr(record_date, 6 , 2)".format(my_q, startDate, endDate))
    elif(startDate != "" and endDate == ""):
        # startDate = datetime.strptime(startDate, "%Y-%m-%d").strftime('%Y-%d-%m')
        # query = query + " where record_date >= '{0}'".format(startDate)
        my_notes = PatientNotes.objects.raw("select id, count(record_date) as month_count, substr(record_date, 6 , 2) as month from reports_patientnotes where history like '%{0}%' and record_date >= '{1}' group by substr(record_date, 6 , 2)".format(my_q, startDate))
    elif(startDate == "" and endDate != ""):
        # endDate = datetime.strptime(endDate, "%Y-%m-%d").strftime('%Y-%d-%m')
        # query = query + " where record_date <= '{0}'".format(endDate)
        my_notes = PatientNotes.objects.raw("select id, count(record_date) as month_count, substr(record_date, 6 , 2) as month from reports_patientnotes where history like '%{0}%' and record_date <= '{1}' group by substr(record_date, 6 , 2)".format(my_q,endDate))
    else:
        my_notes = PatientNotes.objects.raw("select id, count(record_date) as month_count, substr(record_date, 6 , 2) as month from reports_patientnotes where history like '%{0}%' group by substr(record_date, 6 , 2)".format(my_q))
    
    # my_notes = my_notes.filter(
    #     history__icontains=my_q)
    # # print(len(my_notes))
    # # print(my_q)
    if len(my_notes) > 0:
    #     # print(my_notes)
    #     notes = list(my_notes)
    #     # print(notes)
    #     df = pd.DataFrame(notes)
    #     df.record_date = pd.to_datetime(df.record_date)
    #     dg = df.groupby(pd.Grouper(key='record_date', freq='M')).count()
    #     dg.index = dg.index.strftime('%B')
    #     diag_monthly = dg.to_dict()
    #     diag_monthly = diag_monthly['id']
    #     # print(diag_monthly)
        months = ['January', 'February', 'March', 'April', 'May', 'June',
                  'July', 'August', 'September', 'October', 'November', 'December']
        diag_per_month = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        # for my_key in diag_monthly.keys():
        #     index_of_month = months.index(my_key)
        #     diag_per_month[index_of_month] = diag_monthly[my_key]

        for note in my_notes:
            index_of_month = int(note.month)
            diag_per_month[index_of_month-1] = note.month_count

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
    print("FILTER BY ",request.GET.getlist('keys[]'))
    filter_by = request.GET.getlist('keys[]')
    print("FILTER BY ",filter_by)
    response_list = []
    startDate = request.query_params['startDate']
    endDate = request.query_params['endDate']
    my_notes = PatientNotes.objects.values('id', 'record_date', 'history')
    print("DATE FILTER ", startDate)
    query = "select * from reports_patientnotes"
    if(startDate != "" and endDate != ""):
        # startDate = datetime.strptime(startDate, "%Y-%m-%d").strftime('%Y-%m-%d')
        print("UPDATED DATE FILTER ", startDate)
        # endDate = datetime.strptime(endDate, "%Y-%m-%d").strftime('%Y-%m-%d')
        # query = query + " where record_date >= '{0}' and record_date <= '{1}'".format(startDate, endDate)
        my_notes = my_notes.filter(record_date__gte=startDate, record_date__lte=endDate)
    elif(startDate != "" and endDate == ""):
        # startDate = datetime.strptime(startDate, "%Y-%m-%d").strftime('%Y-%d-%m')
        # query = query + " where record_date >= '{0}'".format(startDate)
        my_notes = my_notes.filter(record_date__gte=startDate)
    elif(startDate == "" and endDate != ""):
        # endDate = datetime.strptime(endDate, "%Y-%m-%d").strftime('%Y-%d-%m')
        # query = query + " where record_date <= '{0}'".format(endDate)
        my_notes = my_notes.filter(record_date__lte=endDate)

    # my_notes = PatientNotes.objects.values('id', 'record_date', 'history')
    my_chart = {}
    months = ['January', 'February', 'March', 'April', 'May', 'June',
                  'July', 'August', 'September', 'October', 'November', 'December']
    for my_filter in (filter_by):

        curr_notes = my_notes.filter(history__icontains=my_filter)
         # print(my_notes)
        notes = list(curr_notes)
        # print(notes)
        df = pd.DataFrame(notes)
        df.record_date = pd.to_datetime(df.record_date)
        dg = df.groupby(pd.Grouper(key='record_date', freq='M')).count()
        dg.index = dg.index.strftime('%B')
        diag_monthly = dg.to_dict()
        diag_monthly = diag_monthly['id']
        # print(diag_monthly)
        
        diag_per_month = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        
        
        for my_key in diag_monthly.keys():
            index_of_month = months.index(my_key)
            diag_per_month[index_of_month] = diag_monthly[my_key]

        response = {
            'data': diag_per_month,
            'label': my_filter
        }
        response_list.append(response)
        print(response_list)

    
    my_chart = {
        'label': months,
        'dataset': response_list
    }
    print("RESPONSE HERE")
        # print(months)
        # print(diag_per_month)
    return Response(my_chart)

@api_view(['GET'])
def gender_dist_graph(request):

    startDate = request.query_params['startDate']
    endDate = request.query_params['endDate']
    if(startDate != "" and endDate != ""):
        # startDate = datetime.strptime(startDate, "%Y-%m-%d").strftime('%Y-%m-%d')
        print("UPDATED DATE FILTER ", startDate)
        # endDate = datetime.strptime(endDate, "%Y-%m-%d").strftime('%Y-%m-%d')
<<<<<<< HEAD
        # query = query + " where record_date >= '{0}' and record_date <= '{1}'".format(startDate, endDate)
        db_response = PatientNotes.objects.raw("select id, count(*) as all_count, (select count(*) from reports_patientnotes where history like '%__-year-old male%' or history like '%__-year-old m %' or history like '% y.o.m%' or history like '%y.o. m%' or history like '%yo m %' or history like '% yo man%' or history like '% yo male%' or history like '%yo m,%' or history like '%yo male,%' or history like '% y/o m %' or history like '% y/o male%' or history like '% yo/m%' or history like '% male %' or history like '%yom %' or history like '%year old m%' or history like '%yo m.%' or history like '%yo young man %' or history like '%yo, m %' or history like '% m %' or history like '% yo, m,%' or history like '%yo man%' or history like '%old man%' or history like '%y/o man%' or history like '%yM') and (record_date >= '{0}' and record_date <= '{1}')) as male_count,(select count(*) from reports_patientnotes where (history like '%Female%' or history like '__F%' or history like '_F%' or history like 'female') and (record_date >= '{0}' and record_date <= '{1}')) as female_count from reports_patientnotes limit 1".format(startDate, endDate))[0]
    elif(startDate != "" and endDate == ""):
        # startDate = datetime.strptime(startDate, "%Y-%m-%d").strftime('%Y-%d-%m')
        # query = query + " where record_date >= '{0}'".format(startDate)
        db_response = PatientNotes.objects.raw("select id, count(*) as all_count, (select count(*) from reports_patientnotes where history like '%__-year-old male%' or history like '%__-year-old m %' or history like '% y.o.m%' or history like '%y.o. m%' or history like '%yo m %' or history like '% yo man%' or history like '% yo male%' or history like '%yo m,%' or history like '%yo male,%' or history like '% y/o m %' or history like '% y/o male%' or history like '% yo/m%' or history like '% male %' or history like '%yom %' or history like '%year old m%' or history like '%yo m.%' or history like '%yo young man %' or history like '%yo, m %' or history like '% m %' or history like '% yo, m,%' or history like '%yo man%' or history like '%old man%' or history like '%y/o man%' or history like '%yM') and (record_date >= '{0}')) as male_count,(select count(*) from reports_patientnotes where (history like '%Female%' or history like '__F%' or history like '_F%' or history like 'female') and (record_date >= '{0}' )) as female_count from reports_patientnotes limit 1".format(startDate))[0]
    elif(startDate == "" and endDate != ""):
        # endDate = datetime.strptime(endDate, "%Y-%m-%d").strftime('%Y-%d-%m')
        # query = query + " where record_date <= '{0}'".format(endDate)
        db_response = PatientNotes.objects.raw("select id, count(*) as all_count, (select count(*) from reports_patientnotes where history like '%__-year-old male%' or history like '%__-year-old m %' or history like '% y.o.m%' or history like '%y.o. m%' or history like '%yo m %' or history like '% yo man%' or history like '% yo male%' or history like '%yo m,%' or history like '%yo male,%' or history like '% y/o m %' or history like '% y/o male%' or history like '% yo/m%' or history like '% male %' or history like '%yom %' or history like '%year old m%' or history like '%yo m.%' or history like '%yo young man %' or history like '%yo, m %' or history like '% m %' or history like '% yo, m,%' or history like '%yo man%' or history like '%old man%' or history like '%y/o man%' or history like '%yM') and (record_date <= '{1}')) as male_count,(select count(*) from reports_patientnotes where (history like '%Female%' or history like '__F%' or history like '_F%' or history like 'female') and (record_date <= '{1}')) as female_count from reports_patientnotes limit 1".format(endDate))[0]
    else:
        db_response = PatientNotes.objects.raw("select id, count(*) as all_count, (select count(*) from reports_patientnotes where history like '%__-year-old male%' or history like '%__-year-old m %' or history like '% y.o.m%' or history like '%y.o. m%' or history like '%yo m %' or history like '% yo man%' or history like '% yo male%' or history like '%yo m,%' or history like '%yo male,%' or history like '% y/o m %' or history like '% y/o male%' or history like '% yo/m%' or history like '% male %' or history like '%yom %' or history like '%year old m%' or history like '%yo m.%' or history like '%yo young man %' or history like '%yo, m %' or history like '% m %' or history like '% yo, m,%' or history like '%yo man%' or history like '%old man%' or history like '%y/o man%' or history like '%yM') as male_count,(select count(*) from reports_patientnotes where history like '%Female%' or history like '__F%' or history like '_F%' or history like 'female') as female_count from reports_patientnotes limit 1")[0]
=======
        # query = query + " where record_date >= '{0}' and record_date <= '{1}'".format(startDate, endDate)                
        db_response = PatientNotes.objects.raw("select id, count(*) as all_count, (select count(*) from reports_patientnotes where (history like '% Male %' or history like '___M %' or history like '__M %'  or history like '% yo Male%' or history like '%-year-old Male%' or history like '%y/o Male%' or history like '%y.o Male%'  or history like '% yo M%' or history like '%y/o M%' or history like '%y.o M%' or history like '% m %') and (record_date >= '{0}' and record_date <= '{1}')) as male_count,(select count(*) from reports_patientnotes where history like '% female %' or history like '___F %' or history like '__F %'  or history like '% yo feMale%' or history like '%-year-old feMale%' or history like '%y/o feMale%' or history like '%y.o feMale%' or history like '% yo f%' or history like '%y/o f%' or history like '%y.o f%' or history like '% f %') and (record_date >= '{0}' and record_date <= '{1}')) as female_count from reports_patientnotes limit 1".format(startDate, endDate))[0]
    elif(startDate != "" and endDate == ""):
        # startDate = datetime.strptime(startDate, "%Y-%m-%d").strftime('%Y-%d-%m')
        # query = query + " where record_date >= '{0}'".format(startDate)
        db_response = PatientNotes.objects.raw("select id, (select count(*) from reports_patientnotes where (history like '% Male %' or history like '___M %' or history like '__M %'  or history like '% yo Male%' or history like '%-year-old Male%' or history like '%y/o Male%' or history like '%y.o Male%'  or history like '% yo M%' or history like '%y/o M%' or history like '%y.o M%' or history like '% m %') and (record_date >= '{0}')) as male_count,(select count(*) from reports_patientnotes where (history like '% female %' or history like '___F %' or history like '__F %'  or history like '% yo feMale%' or history like '%-year-old feMale%' or history like '%y/o feMale%' or history like '%y.o feMale%' or history like '% yo f%' or history like '%y/o f%' or history like '%y.o f%') and (record_date >= '{0}')) as female_count from reports_patientnotes limit 1".format(startDate))[0]
    elif(startDate == "" and endDate != ""):
        # endDate = datetime.strptime(endDate, "%Y-%m-%d").strftime('%Y-%d-%m')
        # query = query + " where record_date <= '{0}'".format(endDate)
        db_response = PatientNotes.objects.raw("select id, count(*) as all_count, (select count(*) from reports_patientnotes where (history like '% Male %' or history like '___M %' or history like '__M %'  or history like '% yo Male%' or history like '%-year-old Male%' or history like '%y/o Male%' or history like '%y.o Male%'  or history like '% yo M%' or history like '%y/o M%' or history like '%y.o M%' or history like '% m %') and (record_date <= '{0}')) as male_count,(select count(*) from reports_patientnotes where (history like '% female %' or history like '___F %' or history like '__F %'  or history like '% yo feMale%' or history like '%-year-old feMale%' or history like '%y/o feMale%' or history like '%y.o feMale%' or history like '% yo f%' or history like '%y/o f%' or history like '%y.o f%' or history like '%y.o f%') and (record_date <= '{0}')) as female_count from reports_patientnotes limit 1".format(endDate))[0]
    else:
        db_response = PatientNotes.objects.raw("select id, count(*) as all_count, (select count(*) from reports_patientnotes where history like '% Male %' or history like '___M %' or history like '__M %'  or history like '% yo Male%' or history like '%-year-old Male%' or history like '%y/o Male%' or history like '%y.o Male%'  or history like '% yo M%' or history like '%y/o M%' or history like '%y.o M%' or history like '% m %') as male_count,(select count(*) from reports_patientnotes where history like '% female %' or history like '___F %' or history like '__F %'  or history like '% yo feMale%' or history like '%-year-old feMale%' or history like '%y/o feMale%' or history like '%y.o feMale%' or history like '% yo f%' or history like '%y/o f%' or history like '%y.o f%' or history like '% f %') as female_count from reports_patientnotes limit 1")[0]
>>>>>>> 417cea1189d031ffb7b7580b01c8cd79f062f4a7
    # print("DB RESPONSE = ", db_response.female_count)
    # all_notes = PatientNotes.objects.values('id', 'record_date', 'history')
    male_count = db_response.male_count
    female_count = db_response.female_count
    all_count = db_response.all_count
    # for note in all_notes:
    #     # print(note)
    #     if "male" in note['history'].lower():
    #         male_count += 1

    #     if "female" in note['history'].lower():
    #         female_count += 1

    gender_dist = {
        'male_count': male_count,
        'female_count': female_count,
        'uncategorized': all_count-male_count-female_count
    }
    return Response(gender_dist)


@api_view(['GET'])
def monthly_diagnosis_graph(request):
    
    startDate = request.query_params['startDate']
    endDate = request.query_params['endDate']
    if(startDate != "" and endDate != ""):
        # startDate = datetime.strptime(startDate, "%Y-%m-%d").strftime('%Y-%m-%d')
        print("UPDATED DATE FILTER ", startDate)
        # endDate = datetime.strptime(endDate, "%Y-%m-%d").strftime('%Y-%m-%d')
        # query = query + " where record_date >= '{0}' and record_date <= '{1}'".format(startDate, endDate)
        all_notes = PatientNotes.objects.raw("select '0' as id, count(record_date) as month_count, substr(record_date, 6,2) as month from reports_patientnotes where record_date >= '{0}' and record_date <= '{1}' group by substr(record_date, 6,2)".format(startDate, endDate))
    elif(startDate != "" and endDate == ""):
        # startDate = datetime.strptime(startDate, "%Y-%m-%d").strftime('%Y-%d-%m')
        # query = query + " where record_date >= '{0}'".format(startDate)
        all_notes = PatientNotes.objects.raw("select '0' as id, count(record_date) as month_count, substr(record_date, 6,2) as month from reports_patientnotes where record_date >= '{0}' group by substr(record_date, 6,2)".format(startDate))
    elif(startDate == "" and endDate != ""):
        # endDate = datetime.strptime(endDate, "%Y-%m-%d").strftime('%Y-%d-%m')
        # query = query + " where record_date <= '{0}'".format(endDate)
        all_notes = PatientNotes.objects.raw("select '0' as id, count(record_date) as month_count, substr(record_date, 6,2) as month from reports_patientnotes where record_date <= '{0}' group by substr(record_date, 6,2)".format(endDate))
    else:
        all_notes = PatientNotes.objects.raw("select '0' as id, count(record_date) as month_count, substr(record_date, 6,2) as month from reports_patientnotes group by substr(record_date, 6,2)")


    # all_notes = PatientNotes.objects.values('id', 'record_date', 'history')
    # df = pd.DataFrame(all_notes)
    # df.record_date = pd.to_datetime(df.record_date)
    # dg = df.groupby(pd.Grouper(key='record_date', freq='1M')).count()
    # dg.index = dg.index.strftime('%B')
    # diag_monthly = dg.to_dict()
    # diag_monthly = diag_monthly['id']
    # print(diag_monthly)
    months = ['January', 'February', 'March', 'April', 'May', 'June',
              'July', 'August', 'September', 'October', 'November', 'December']

    diag_per_month = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

    for note in all_notes:
        index_of_month = int(note.month)
        print(index_of_month, note.month_count)
        diag_per_month[index_of_month-1] = note.month_count


    
    # for my_key in diag_monthly.keys():
    #     index_of_month = months.index(my_key)
    #     diag_per_month[index_of_month] = diag_monthly[my_key]

    monthlydist = {
        'keys': months,
        'values': diag_per_month
    }

    return Response(monthlydist)

@api_view(['GET'])
def age_dist(request):

    startDate = request.query_params['startDate']
    endDate = request.query_params['endDate']

    print("DATE FILTER ", startDate)
    query = "select * from reports_patientnotes"
    if(startDate != "" and endDate != ""):
        # startDate = datetime.strptime(startDate, "%Y-%m-%d").strftime('%Y-%m-%d')
        print("UPDATED DATE FILTER ", startDate)
        # endDate = datetime.strptime(endDate, "%Y-%m-%d").strftime('%Y-%m-%d')
        query = query + " where record_date >= '{0}' and record_date <= '{1}'".format(startDate, endDate)
    elif(startDate != "" and endDate == ""):
        # startDate = datetime.strptime(startDate, "%Y-%m-%d").strftime('%Y-%d-%m')
        query = query + " where record_date >= '{0}'".format(startDate)
    elif(startDate == "" and endDate != ""):
        # endDate = datetime.strptime(endDate, "%Y-%m-%d").strftime('%Y-%d-%m')
        query = query + " where record_date <= '{0}'".format(endDate)
    print("QUERY= ", query)
    all_notes = PatientNotes.objects.raw(query)
    age_data = [0, 0, 0, 0, 0, 0]
    age_trailing_vars = ["yo", "y.o", "y/o",
                         "year-old", "year old", "years old", "-year-old", " y.o", " yo", " year old", " y o", " y/o", " y.o"]
    for note in all_notes:
        # print(note)
        age_var_found = []
        for my_var in age_trailing_vars:
            if my_var in note.history:
                age_var_found.append(my_var)
        # print(age_var_found)
        if len(age_var_found) > 0:
            my_index = note.history.index(age_var_found[0])
            age_strs = []
            age_strs.append(note.history[my_index-3])
            age_strs.append(note.history[my_index-2])
            age_strs.append(note.history[my_index-1])
            for age_str in age_strs:
                if not age_str.isnumeric():
                    age_strs.remove(age_str)
            
            if ''.join(age_strs).isnumeric():
                age = int(''.join(age_strs))
                if age < 6:
                    age_data[0] += 1
                elif age >= 6 and age <= 13:
                    age_data[1] += 1
                elif age >= 14 and age <= 21:
                    age_data[2] += 1
                elif age >= 22 and age <= 35:
                    age_data[3] += 1
                elif age >= 36 and age <= 49:
                    age_data[4] += 1
                else:
                    age_data[5] += 1
            # print(age)
            # print(age_data)

    age_labels = ["0-5", "6-13", "14-21", "22-35", "35-49", "50+"]
    response = {
        'labels': age_labels,
        'data': age_data,
    }

    return Response(response)

@api_view(['GET'])
def most_freq(request):

   
    all_notes = PatientNotes.objects.values('id', 'record_date', 'history')
    all_count = all_notes.count()
    startDate = request.query_params['startDate']
    endDate = request.query_params['endDate']
    if(request.query_params['genderFilter'] == 'uncategorized'):
        print("BEFORE FILTER SIZE", all_notes.count())
        all_notes = all_notes.exclude(history__icontains = ' male ')
        print("FIRST FILTER SIZE", all_notes.count())
        all_notes = all_notes.exclude(history__icontains = ' female ')
        print("SECOND FILTER SIZE", all_notes.count())
    elif(request.query_params['genderFilter'] != 'default'):
        all_notes = all_notes.filter(history__icontains = request.query_params['genderFilter'])
    if(startDate != "" and endDate != ""):
        # startDate = datetime.strptime(startDate, "%Y-%m-%d").strftime('%Y-%m-%d')
        print("UPDATED DATE FILTER ", startDate)
        # endDate = datetime.strptime(endDate, "%Y-%m-%d").strftime('%Y-%m-%d')
        all_notes = all_notes.filter(record_date__gte=startDate, record_date__lte=endDate)
    elif(startDate != "" and endDate == ""):
        # startDate = datetime.strptime(startDate, "%Y-%m-%d").strftime('%Y-%d-%m')
        all_notes = all_notes.filter(record_date__gte=startDate)
    elif(startDate == "" and endDate != ""):
        # endDate = datetime.strptime(endDate, "%Y-%m-%d").strftime('%Y-%d-%m')
        all_notes = all_notes.filter(record_date__lte=endDate)
     
    words_list = [{"text": 'Abdominal Pain', "count": 0}, {"text": 'Stomach Ache', "count": 0}, {"text": 'Headache', "count": 0}, {"text": 'Dizziness', "count": 0}, {"text": 'Fever', "count": 0}, {
        "text": 'Cough', "count": 0}, {"text": 'Palpitations', "count": 0}, {"text": 'nausea', "count": 0}, {"text": 'vomiting', "count": 0}, {"text": 'anxiety', "count": 0}]
    
    
    for word in words_list:
        for note in all_notes:
            if word["text"].lower() in note['history'].lower():
                word["count"] += 1
    

    # for word in words_list:
    #     all_notes = PatientNotes.objects.raw("select id, count(*) as counts, history from reports_patientnotes where lower(history) like '%{0}%'".format(word["text"].lower()))[0]
    #     # print("NOTES = ", count_notes)
    #     word["count"] = all_notes.counts

    sorted_words = sorted(words_list, key=lambda d: d['count'], reverse=True)
    top5 = sorted_words[:5]
    
    # print(top5)

    top5_labels = list(map(lambda t: t["text"].capitalize(), top5))
    top5_data = list(map(lambda t: t["count"], top5))
    
    # print(top5_labels, top5_data)
    
    response = {
        'labels': top5_labels,
        'data': top5_data,
    }

    return Response(response)
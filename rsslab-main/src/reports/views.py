from django.shortcuts import render, redirect
import pandas as pd

from .models import PatientNotes
from django.contrib.auth.decorators import login_required

from .forms import CsvUploadForm

from django.contrib import messages


@login_required
def upload_file(request):
    if request.method == "POST":
        form = CsvUploadForm(request.POST, request.FILES)
        print(request.POST)
        if form.is_valid():
            # print(form.cleaned_data)
            form.save()
            messages.add_message(
                request, messages.SUCCESS, 'CSV Saved Successfully.')
            return redirect('index')
    else:
        form = CsvUploadForm()

    return render(request, 'upload.html', {'form': form})


@login_required
def index(request):
    return redirect('upload')


@login_required
def reports_all(request):
    all_notes = PatientNotes.objects.values('id', 'record_date', 'history')
    # # Calculating Monthly Diagnosis
    notes = list(all_notes)
    # # print(notes)
    # df = pd.DataFrame(notes)
    # df.record_date = pd.to_datetime(df.record_date)
    # dg = df.groupby(pd.Grouper(key='record_date', freq='1M')).count()
    # dg.index = dg.index.strftime('%B')
    # diag_monthly = dg.to_dict()
    # diag_monthly = diag_monthly['id']
    # # print(diag_monthly)
    # months = ['January', 'February', 'March', 'April', 'May', 'June',
    #           'July', 'August', 'September', 'October', 'November', 'December']
    # diag_per_month = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    # for my_key in diag_monthly.keys():
    #     index_of_month = months.index(my_key)
    #     diag_per_month[index_of_month] = diag_monthly[my_key]

    # print(diag_monthly)
    # for month in months:
    #     try:
    #         if diag_monthly[month]:
    #             my_diag_monthly[month] = diag_monthly[month]
    #             # print(f'{month} is present.')
    #     except KeyError:
    #         my_diag_monthly[month] = 0

    # if diag_monthly['id']['Jan']:
    # print("Jan is here")
    # charts = {}
    # charts['diag_monthly'] = {
    #     # 'keys': list(my_diag_monthly.keys()),
    #     'keys': months,
    #     # 'values': list(my_diag_monthly.values())
    #     'values': diag_per_month
    # }
    # Male Female Graph Calculations
    # male_count = 0
    # female_count = 0
    # for note in all_notes:
    #     # print(note)
    #     if "male" in note['history'].lower():
    #         male_count += 1

    #     if "female" in note['history'].lower():
    #         female_count += 1

    # # total_count = male_count + female_count
    # # if total_count > 0:
    # #     male_percentage = (male_count/total_count)*100
    # #     female_percentage = (female_count/total_count)*100
    # # else:
    # #     male_percentage = 0
    # #     female_percentage = 0

    # charts['gender_dist'] = {
    #     'male': male_count,
    #     'female': female_count,
    # }
    # Calculating Breakdown by Age
    # age_data = [0, 0, 0, 0, 0, 0]
    # age_trailing_vars = ["yo", 'y.o', 'y/o',
    #                      'year-old', 'year old', 'years old']
    # for note in all_notes:
    #     # print(note)
    #     age_var_found = []
    #     for my_var in age_trailing_vars:
    #         if my_var in note['history']:
    #             age_var_found.append(my_var)
    #     # print(age_var_found)
    #     if len(age_var_found) > 0:
    #         my_index = note['history'].index(age_var_found[0])
    #         age_strs = []
    #         age_strs.append(note["history"][my_index-3])
    #         age_strs.append(note["history"][my_index-2])
    #         age_strs.append(note["history"][my_index-1])
    #         for age_str in age_strs:
    #             if not age_str.isnumeric():
    #                 age_strs.remove(age_str)
            
    #         if ''.join(age_strs).isnumeric():
    #             age = int(''.join(age_strs))
    #             if age < 6:
    #                 age_data[0] += 1
    #             elif age >= 6 and age <= 13:
    #                 age_data[1] += 1
    #             elif age >= 14 and age <= 21:
    #                 age_data[2] += 1
    #             elif age >= 22 and age <= 35:
    #                 age_data[3] += 1
    #             elif age >= 36 and age <= 49:
    #                 age_data[4] += 1
    #             else:
    #                 age_data[5] += 1
    #         # print(age)
    #         # print(age_data)

    #     age_labels = ["0-5", "6-13", "14-21", "22-35", "35-49", "50+"]
    #     charts['age'] = {
    #         'labels': age_labels,
    #         'data': age_data,
    #     }

    # Create top 5 symptoms graph
    # words_list = [{"text": 'Abdominal Pain', "count": 0}, {"text": 'Stomach Ache', "count": 0}, {"text": 'Head ache', "count": 0}, {"text": 'Dizziness', "count": 0}, {"text": 'Fever', "count": 0}, {
    #     "text": 'Cough', "count": 0}, {"text": 'Palpitations', "count": 0}, {"text": 'nausea', "count": 0}, {"text": 'vomiting', "count": 0}, {"text": 'anxiety', "count": 0}]
    # for word in words_list:
    #     for note in all_notes:
    #         if word["text"].lower() in note['history'].lower():
    #             word["count"] += 1
    # sorted_words = sorted(words_list, key=lambda d: d['count'], reverse=True)
    # top5 = sorted_words[:5]
    # # print(top5)

    # top5_labels = list(map(lambda t: t["text"].capitalize(), top5))
    # top5_data = list(map(lambda t: t["count"], top5))
    # # print(top5_labels, top5_data)
    # charts["freq_symptoms"] = {
    #     'labels': top5_labels,
    #     'data': top5_data,
    # }

    context = {
        'notes': len(notes)
    }

    return render(request, 'index.html', context)

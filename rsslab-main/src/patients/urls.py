from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from . import settings

from reports.views import reports_all, index, upload_file

from api.views import filtered_patients_data, search_records, basicdash, gender_dist_graph, monthly_diagnosis_graph, age_dist, most_freq

urlpatterns = [
    path('', index, name='index'),
    path('upload', upload_file, name='upload'),
    path('reports', reports_all, name='reports'),
    path('api-symptoms', filtered_patients_data, name='api-symptoms'),
    path('api-search', search_records, name='api-search'),
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('basicdash', basicdash, name = 'basicdash'),
    path('gender-dist', gender_dist_graph, name="genderdist"),
    path('monthly',monthly_diagnosis_graph, name="monthlydist"),
    path('age-dist', age_dist, name="agedist"),
    path('most-freq', most_freq, name="most_freq")
    
]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)

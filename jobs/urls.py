from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('jobsapp.urls')),
    path('', include('accounts.urls')),
    path('api/', include([
        path('', include('jobsapp.api.urls')),
    ])),
]

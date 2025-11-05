from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path('accounts/', include('accounts.urls')),
    # optional: include auth urls for password reset, logout, etc.
    path('accounts/', include('django.contrib.auth.urls')),
]

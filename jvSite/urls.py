
from django.contrib import admin
from django.urls import path, include
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from jsite.views import HomeView, AboutView, NoticeView, ContactView
from jsite import views

urlpatterns = [
    path('admin/', admin.site.urls, name = 'admin'),
    path('', HomeView.as_view(), name='home'),
    path('about', AboutView.as_view(), name='about'),
    path('notice', NoticeView.as_view(), name='notice'),
    path('contact', ContactView.as_view(), name='contact'),
    path('results', views.result_view, name='results'),
    path('students/', include('students.urls')),



]
urlpatterns += staticfiles_urlpatterns()

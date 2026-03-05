from django.contrib import admin
from django.urls import path,include
from myapp import views
urlpatterns=[
    path('index/',views.index,name='index'),
    # path('test/',views.send_test_email,name='send_test_email'),
    path('test/',views.homepage,name='send_test_email')

]
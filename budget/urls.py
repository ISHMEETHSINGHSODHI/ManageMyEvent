from django.contrib import admin
from django.urls import path,include
from .import views

urlpatterns = [
   path('',views.project_list,name = 'list'),
   path('add', views.ProjectCreateView.as_view(),name ='add'),
   path('<slug:project_slug>',views.project_detail,name='detail'),
   path('bar/',views.export_data_and_generate_plots,name='export_data_and_generate_plots'),
   path('download-graph/', views.download_graph_view, name='download_graph'),
   path('send_email/', views.homepage, name='send_email'),

]
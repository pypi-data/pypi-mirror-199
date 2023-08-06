from django.urls import path
from . import views

urlpatterns = [
	path('list/', views.LogList, name="log-list"),
	path('detail/<str:hashid>/', views.LogDetail, name="log-detail"),
]
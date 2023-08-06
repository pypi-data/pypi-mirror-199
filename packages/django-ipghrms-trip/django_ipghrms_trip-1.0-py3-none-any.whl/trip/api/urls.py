from django.urls import path
from . import views

urlpatterns = [
    path('cat/', views.APIContEmpTrip.as_view(), name="cont-api-emp-tip"),  
    path('cat/tot/', views.APITripTotal.as_view(), name="cont-api-emp-tip-tot"),  
]
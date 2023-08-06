from django.urls import path
from . import views

urlpatterns = [
    path('dash/', views.vTripDash, name='t-dash'),
    path('list/', views.vTripList, name='t-list'),
    path('summary/', views.vTripSummary, name='t-summary'),
    path('add/', views.mTripAdd, name='m-t-add'),
    path('update/<str:hashid>/', views.mTripUpdate, name='m-t-update'),
    path('detail/<str:hashid>/', views.mTripDetail, name='m-t-detail'),
    path('lock/<str:hashid>/', views.mTripLock, name='m-t-lock'),
    path('emp/add/<str:hashid>/', views.mTripEmpAdd, name='m-t-emp-add'),
    path('emp/update/<str:hashid>/', views.mTripEmpUpdate, name='m-t-emp-udpate'),
    path('emp/delete/<str:hashid>/', views.mTripEmpDelete, name='m-t-emp-delete'),
    path('emp/update/att/<str:hashid>/<int:pk>/', views.hrTripUpdateAtt, name='m-t-emp-update-att'),
    path('delete/<str:hashid>/', views.hrTripDeleteAtt, name='m-t-delete'),
]
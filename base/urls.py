from django.urls import path
from base import views


urlpatterns = [
    path('', views.home, name='home'),
    path('create-account/', views.create_account, name='create-account'),
    path('log-in/', views.log_in, name='log_in'),
    path('account/<str:pk>/', views.account, name='account'),
    path('edit/<str:pk>/', views.edit, name='edit'),
    path('payment/<str:pk>/', views.payment, name='payment'),
    path('Add/<str:pk>/', views.add, name='Add'),
    path('history/<str:pk>/', views.history, name='history'),
    path('history_data/<str:pk>/<str:sk>/', views.history_data, name='history_data'),
    path('history_add/<str:pk>/<str:sk>/', views.history_add, name='add_history'),
    path('User-account/<str:pk>/', views.user_account, name='user-account'),
    path('status/', views.status, name='status')
]
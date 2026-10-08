from django.urls import path
from . import views

urlpatterns = [
	path('registration/', views.user_registration, name='registration' ),
	path('dashboard/', views.dashboard, name='dashboard'),
	path('login/', views.login, name='login'),
	path('record_transaction/', views.record_transaction, name='record_transaction'),

]
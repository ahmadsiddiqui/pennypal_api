from django.shortcuts import render
from api.models import *

def user_registration(request):
	return render(request, 'frontend/registration.html')

def dashboard(request):
	return render(request, 'frontend/dashboard.html')

def login(request):
	return render(request, 'frontend/login.html')

def record_transaction(request):
	context = {}
	context['categories'] = Category.objects.all()
	context['payment_modes'] = Transaction.PaymentModes.choices
	context['transaction_types'] = Transaction.TransactionTypes.choices
	

	return render(request, 'frontend/record_transaction.html', context)

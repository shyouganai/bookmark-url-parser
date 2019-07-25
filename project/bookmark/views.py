from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.views.generic.base import View

class RegistrationView(View):

	def get(self, request, *args, **kwargs):
		return render(request,
			'registration/registration.html')

	def post(self, request, *args, **kwargs):
		if not User.objects.filter(username=request.POST['username']):
			user = User.objects.create_user(
				username = request.POST['username'],
				email = request.POST['email'],
				password = request.POST['password'],
				first_name = request.POST['first_name'],
				last_name = request.POST['last_name'])
			user.save()
			return redirect('login')
		return redirect('register')
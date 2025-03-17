from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.db import models
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from charity_donations_app.models import Institution, Donation


class LandingPage(View):
    def get(self, request):
        foundations = Institution.objects.filter(type=Institution.FOUNDATION)
        ngos = Institution.objects.filter(type=Institution.NGO)
        local_collections = Institution.objects.filter(type=Institution.LOCAL_COLLECTION)
        
        bags_given = Donation.objects.aggregate(total_bags=models.Sum('quantity'))['total_bags'] or 0
        organizations_supported = Institution.objects.count()

        context = {
            'foundations': foundations,
            'ngos': ngos,
            'local_collections': local_collections,
            'bags_given': bags_given,
            'organizations_supported': organizations_supported
        }
        return render(request, 'index.html', context)


class AddDonation(View):
    def get(self, request):
        return render(request, 'form.html')
    

class UserProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'user_profile.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        return context

    
class Logout(View):
    def get(self, request):
        logout(request)
        return redirect('landing')


class Login(View):
    def get(self, request):
        return render(request, 'login.html')

    def post(self, request):
        email = request.POST.get("email")
        password = request.POST.get("password")
        
        if not email or not password:
            messages.error(request, "Proszę podać adres email i hasło.")
            return render(request, 'login.html')
        
        user = User.objects.filter(email=email).first()
        
        if user is None:
            messages.error(request, "Nie znaleziono użytkownika. Przekierowanie do rejestracji.")
            return redirect('register')
        
        user = authenticate(request, username=user.username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('landing')
        else:
            messages.error(request, "Błędne dane logowania.")
            return render(request, 'login.html')


class Register(View):
    def get(self, request):
        return render(request, 'register.html')

    def post(self, request):
        name = request.POST.get("name")
        surname = request.POST.get("surname")
        email = request.POST.get("email")
        password = request.POST.get("password")
        password2 = request.POST.get("password2")

        if password != password2:
            messages.error(request, "Passwords are not the same.")
            return render(request, 'register.html')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email unavailable.")
            return render(request, 'register.html')

        user = User.objects.create_user(username=email, email=email, password=password)
        user.first_name = name
        user.last_name = surname
        user.save()
        return redirect('login')
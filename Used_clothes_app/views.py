from typing import Any

from django.core.paginator import Paginator
from django.forms import forms, formset_factory
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views import View
from django.contrib.auth import authenticate, login, logout
from Used_clothes_app.models import Institution, Donation, Category
from Used_clothes_app.form import LoginForm, RegistrationForm, ProfileForm, DonationForm


class LandingPage(View):
    def get(self, request):
        fundactions_list = Institution.objects.filter(
            type="f").order_by("-name")
        non_gov_orgs_list = Institution.objects.filter(
            type="op").order_by("-name")
        locall_collections_list = Institution.objects.filter(
            type="zl").order_by("-name")

        f = Paginator(fundactions_list, 3)
        page_1 = request.GET.get("page")
        fundactions = f.get_page(page_1)

        n = Paginator(non_gov_orgs_list, 3)
        page_2 = request.GET.get("page")
        non_gov_orgs = n.get_page(page_2)

        l = Paginator(locall_collections_list, 3)
        page_3 = request.GET.get("page")
        locall_collections = l.get_page(page_3)

        donations = Donation.objects.all()
        bag_quantity = 0
        for donation in donations:
            bag_quantity += donation.quantity

        fundactions_name = [don.institution.name for don in donations]
        fundactions_set = set(fundactions_name)
        fundactions_name_count = len(list(fundactions_set))

        user = request.user
        if user.is_authenticated:
            ctx = {
                'fundactions': fundactions,
                'non_gov_orgs': non_gov_orgs,
                'locall_collections': locall_collections,
                'bag_quantity': bag_quantity,
                'fundactions_name_count': fundactions_name_count,
                'user': user,
            }
        else:
            ctx = {
                'fundactions': fundactions,
                'non_gov_orgs': non_gov_orgs,
                'locall_collections': locall_collections,
                'bag_quantity': bag_quantity,
                'fundactions_name_count': fundactions_name_count,
            }

        return render(request, 'index.html', ctx)


class AddDonation(View):
    def get(self, request):

        categories = Category.objects.all()
        institutions = Institution.objects.all()

        ctx = {
            'categories': categories,
            'institutions': institutions,
        }
        return render(request, 'form.html', ctx)

    def post(self, request):

        form = DonationForm(request.POST)
        if form.is_valid():
            donation = Donation()
            donation.quantity = form.cleaned_data['quantity']
            institution = get_object_or_404(
                Institution, pk=form.cleaned_data['institution'])
            donation.institution = institution
            donation.address = form.cleaned_data['address']
            donation.phone_number = form.cleaned_data['phone_number']
            donation.city = form.cleaned_data['city']
            donation.zip_code = form.cleaned_data['zip_code']
            donation.pick_up_date = form.cleaned_data['pick_up_date']
            donation.pick_up_time = form.cleaned_data['pick_up_time']
            donation.pick_up_comment = form.cleaned_data['pick_up_comment']
            donation.user = request.user
            donation.save()
            categories = Category.objects.filter(
                pk__in=form.cleaned_data['categories'])
            donation.categories.set(categories)

            return JsonResponse({'status': 'success', 'success_url': reverse('success')})
        else:
            return JsonResponse({'status': 'error', 'errors': form.errors})


class Register(View):
    '''
    Registration views. Generate form to fill information and save them to
    postgres database
    if success:
    return redirect to login view
    if error:
    return form again
    '''

    def get(self, request):
        form = RegistrationForm()
        ctx = {
            "form": form,
        }
        return render(request, "register.html", ctx)

    def post(self, request):
        form = RegistrationForm(request.POST)
        ctx = {
            "form": form,
        }
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            return redirect('login')
        else:
            print(form.errors)
        return render(request, 'register.html', ctx)


class Login(View):
    '''
    Render login form. On post side check password and authorize user.
    If password is the same in both form fields:
    return redirect to home view
    If password is wrong:
    return form again
    '''

    def get(self, request):
        form = LoginForm()
        ctx = {
            "form": form,
        }
        return render(request, 'login.html', ctx)

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('landing-page')
            else:
                return redirect('register')


class Logout(View):
    '''
    Logout user. After logout. Display success message
    return redirect to login views
    '''

    def get(self, request):
        logout(request)
        return redirect('login')


class Profile(View):
    def get(self, request):
        user = request.user
        donations = user.donation_set.all()
        ctx = {
            'user': user,
            'donations': donations,
        }
        return render(request, 'profile.html', ctx)

    def post(self, request):
        user = request.user
        donations = user.donation_set.all()
        for donation in donations:
            id = donation.id        
            donation_is_taken = request.POST.get(id)
            donation = get_object_or_404(Donation, id=id)
            donation.is_taken = True if donation_is_taken else False
            donation.save()
        
        return redirect('profile')


class FormConfirmation(View):
    def get(self, request):
        return render(request, 'form-confirmation.html')

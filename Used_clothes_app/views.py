from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import authenticate, login, logout
from Used_clothes_app.models import Institution, Donation, Category
from Used_clothes_app.form import LoginForm, RegistrationForm


class LandingPage(View):
    def get(self, request):
        fundactions_list = Institution.objects.filter(type="f").order_by("-name")
        non_gov_orgs_list = Institution.objects.filter(type="op").order_by("-name")
        locall_collections_list = Institution.objects.filter(type="zl").order_by("-name")

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
        for donation in donations: bag_quantity += donation.quantity

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

        category = Category.objects.all()
        institutions = Institution.objects.all()

        ctx = {
            'category': category,
            'institutions': institutions,
        }
        return render(request, 'form.html', ctx)


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
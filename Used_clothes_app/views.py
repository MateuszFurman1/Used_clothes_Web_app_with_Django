from urllib import request
from django.core.paginator import Paginator
from django.shortcuts import render
from django.views import View

from Used_clothes_app.models import Institution, Donation


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
        return render(request, 'form.html')


class Login(View):
    def get(self, request):
        return render(request, 'login.html')


class Register(View):
    def get(self, request):
        return render(request, 'register.html')

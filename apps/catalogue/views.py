from django.shortcuts import render
from django.http import HttpResponse

from catalogue.models import Etudiant
# Create your views here.



def index(request):
    list_etud_Garcons= Etudiant.objects.filter(titre__exact="M")
    context={'etud_garcons': list_etud_Garcons}
    return render(request, 'catalogue/index.html', context=context)



from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Livre, Auteur, Etudiant, Exemplaire
from .forms import LivreForm



def index(request):
    """Page d'accueil centralisant les statistiques et les accès rapides."""
    # Comptage des métriques
    num_livres = Livre.objects.count()
    num_exemplaires = Exemplaire.objects.count()
    num_exemplaires_dispo = Exemplaire.objects.filter(status='d').count()
    num_auteurs = Auteur.objects.count()
    num_etudiants = Etudiant.objects.count()
    
    # Récupération des 5 derniers livres ajoutés au catalogue
    derniers_livres = Livre.objects.select_related('auteur').order_by('-id')[:5]

    context = {
        'num_livres': num_livres,
        'num_exemplaires': num_exemplaires,
        'num_exemplaires_dispo': num_exemplaires_dispo,
        'num_auteurs': num_auteurs,
        'num_etudiants': num_etudiants,
        'derniers_livres': derniers_livres,
    }

    return render(request, 'index.html', context)

def liste_livres(request):
    """Affiche la liste des livres avec recherche et pagination."""
    query = request.GET.get('q', '')
    
    # Optimisation de la requête SQL (évite le problème N+1)
    livres_list = Livre.objects.select_related('auteur').prefetch_related('genre').all()

    # Application du filtre de recherche si une requête existe
    if query:
        livres_list = livres_list.filter(
            Q(titre__icontains=query) |
            Q(auteur__nom__icontains=query) |
            Q(auteur__prenoms__icontains=query) |
            Q(isbn__icontains=query)
        ).distinct()

    # Gestion manuelle de la pagination (10 livres par page)
    paginator = Paginator(livres_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'livres': page_obj,          # Les livres de la page courante
        'page_obj': page_obj,        # Objet pagination pour le template
        'is_paginated': page_obj.has_other_pages(),
        'query': query,              # Garde le terme recherché dans la barre
    }
    
    return render(request, 'catalogue/livre_list.html', context)


def detail_livre(request, pk):
    """Affiche la fiche détaillée d'un livre et ses exemplaires."""
    # get_object_or_404 renvoie une erreur 404 propre si l'ID n'existe pas
    livre = get_object_or_404(Livre, pk=pk)
    
    # Récupération des exemplaires liés
    exemplaires = livre.exemplaire_set.all()
    nombre_disponibles = exemplaires.filter(status='d').count()

    context = {
        'livre': livre,
        'exemplaires': exemplaires,
        'nombre_disponibles': nombre_disponibles,
    }
    
    return render(request, 'catalogue/livre_detail.html', context)



def ajouter_livre(request):
    """Affiche et traite le formulaire d'ajout d'un livre."""
    if request.method == 'POST':
        form = LivreForm(request.POST)
        if form.is_valid():
            livre = form.save()  # Enregistre directement le livre en BDD
            return redirect('detail_livre', pk=livre.pk)
    else:
        form = LivreForm()  # Formulaire vide en GET

    return render(request, 'catalogue/livre_form.html', {'form': form, 'titre_page': 'Ajouter un Livre'})
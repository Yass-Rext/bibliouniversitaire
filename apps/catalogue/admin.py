from django.contrib import admin
from .models import Etudiant, Genre, Auteur, Livre, Exemplaire


# -----------------------------------------------------------------------------
# Inline : Permet d'ajouter/modifier des exemplaires DIRECTEMENT dans le livre
# -----------------------------------------------------------------------------
class ExemplaireInline(admin.TabularInline):
    """Affiche la liste des exemplaires physiques directement dans la page du livre."""
    model = Exemplaire
    extra = 1  # Laisse une ligne vide pour ajouter un exemplaire rapidement
    fields = ('numero_exemplaire', 'status', 'date_retour', 'emprunteur')


# -----------------------------------------------------------------------------
# Configuration de l'administration pour chaque modèle
# -----------------------------------------------------------------------------

@admin.register(Etudiant)
class EtudiantAdmin(admin.ModelAdmin):
    # Colonnes affichées dans le tableau récapitulatif
    list_display = ('nom', 'prenom', 'titre', 'email')
    # Barre de recherche (sur le nom, prénom et l'email)
    search_fields = ('nom', 'prenom', 'email')
    # Filtre sur le côté
    list_filter = ('titre',)


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('nom',)
    search_fields = ('nom',)


@admin.register(Auteur)
class AuteurAdmin(admin.ModelAdmin):
    list_display = ('nom', 'prenoms', 'date_naissance', 'date_de_deces')
    search_fields = ('nom', 'prenoms')
    fields = ['prenoms', 'nom', ('date_naissance', 'date_de_deces')]  # Met les dates sur la même ligne


@admin.register(Livre)
class LivreAdmin(admin.ModelAdmin):
    list_display = ('titre', 'auteur', 'isbn', 'afficher_genres')
    search_fields = ('titre', 'isbn', 'auteur__nom', 'auteur__prenoms')
    list_filter = ('genre', 'auteur')
    # Permet de sélectionner les genres avec une double liste très pratique
    filter_horizontal = ('genre',)
    # Intègre la gestion des exemplaires directement dans la fiche du livre
    inlines = [ExemplaireInline]

    def afficher_genres(self, obj):
        """Affiche les genres sous forme de chaîne de caractères dans la liste."""
        return ", ".join([genre.nom for genre in obj.genre.all()])
    afficher_genres.short_description = 'Genre(s)'


@admin.register(Exemplaire)
class ExemplaireAdmin(admin.ModelAdmin):
    list_display = ('numero_exemplaire', 'livre', 'status', 'emprunteur', 'date_retour')
    list_filter = ('status', 'date_retour')
    search_fields = (
        'numero_exemplaire', 
        'livre__titre', 
        'emprunteur__nom', 
        'emprunteur__prenom'
    )
    
    # Organisation des champs dans le formulaire d'édition
    fieldsets = (
        ('Informations Générales', {
            'fields': ('livre', 'numero_exemplaire', 'id')
        }),
        ('Disponibilité & Prêt', {
            'fields': ('status', 'date_retour', 'emprunteur')
        }),
    )
    # Rendre l'UUID (id) lisible mais non modifiable manuellement
    readonly_fields = ('id',)
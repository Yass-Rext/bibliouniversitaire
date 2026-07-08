from django.contrib import admin
from catalogue.models import Genre, Livre, Exemplaire, Auteur, Etudiant

# Register your models here.
admin.site.register(Genre)
admin.site.register(Livre)
admin.site.register(Exemplaire)
admin.site.register(Etudiant)
admin.site.register(Auteur)

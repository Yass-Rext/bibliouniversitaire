from django import forms
from .models import Livre, Auteur, Etudiant, Exemplaire


class LivreForm(forms.ModelForm):
    """Formulaire de création et modification d'un livre."""
    class Meta:
        model = Livre
        fields = ['titre', 'auteur', 'resume', 'isbn', 'genre']
        widgets = {
            'titre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Titre du livre'}),
            'auteur': forms.Select(attrs={'class': 'form-select'}),
            'resume': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Résumé du livre'}),
            'isbn': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: 9782123456789'}),
            'genre': forms.SelectMultiple(attrs={'class': 'form-select', 'size': '5'}),
        }


class AuteurForm(forms.ModelForm):
    """Formulaire pour ajouter un auteur."""
    class Meta:
        model = Auteur
        fields = ['prenoms', 'nom', 'date_naissance', 'date_de_deces']
        widgets = {
            'prenoms': forms.TextInput(attrs={'class': 'form-control'}),
            'nom': forms.TextInput(attrs={'class': 'form-control'}),
            'date_naissance': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'date_de_deces': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }


class EtudiantForm(forms.ModelForm):
    """Formulaire d'inscription d'un étudiant."""
    class Meta:
        model = Etudiant
        fields = ['titre', 'nom', 'prenom', 'email']
        widgets = {
            'titre': forms.Select(attrs={'class': 'form-select'}),
            'nom': forms.TextInput(attrs={'class': 'form-control'}),
            'prenom': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'etudiant@univ.sn'}),
        }


class EmpruntForm(forms.Form):
    """Formulaire simple pour enregistrer l'emprunt d'un exemplaire."""
    etudiant = forms.ModelChoiceField(
        queryset=Etudiant.objects.all(),
        label="Sélectionner l'étudiant",
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    date_retour = forms.DateField(
        label="Date de retour prévue",
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'})
    )
import uuid
from django.db import models
from django.urls import reverse

# Create your models here.

class Etudiant(models.Model):
    nom = models.CharField(max_length=40, help_text="Entrez le nom de l'étudiant")
  #  prenom = models.CharField(max_length=100,help_text="Entrez le prénom de l'étudiant")
   # email = models.EmailField(unique=True,help_text="Entrez l'email de l'étudiant")
    type_titre=(
        ('M', 'Monsieur'),
        ('Mme', 'Madame'),
        ('Mlle', 'Mademoiselle'),
    )
    titre= models.CharField(max_length=10, choices=type_titre, help_text="Selectionnez le titre de l'étudiant")
    
    #def __str__(self):
     #   return f"{self.prenom} {self.nom}"

class Genre(models.Model):
    nom = models.CharField(max_length=200,help_text="Entrez le nom du genre d'un livre ex: Littérrature, Science-fiction, etc.")

    def __str__(self):
        return self.nom

class Livre(models.Model):
    titre=models.CharField(max_length=200,help_text="Entrez le titre du livre")
    auteur=models.ForeignKey('Auteur', on_delete=models.SET_NULL, null=True, help_text="Entrez le nom de l'auteur du livre")
    resume=models.TextField(max_length=1000, help_text="Entrez le résumé du livre")
    isbn=models.CharField('ISBN', max_length=13, unique=True, help_text="Entrez l'ISBN du livre")
    genre=models.ManyToManyField(Genre, help_text="Sélectionnez le genre du livre")
    
    def __str__(self):
        return self.titre
    def get_absolute_url(self):
        return reverse('detail_livre', args=[str(self.id)])
    
    
class Exemplaire(models.Model):
    id= models.UUIDField(primary_key=True, default=uuid.uuid4, help_text="Identifiant unique de l'exemplaire")
    livre = models.ForeignKey('Livre', on_delete=models.SET_NULL, null=True, help_text="Sélectionnez le livre")
    date_retour= models.DateField(null=True, blank=True, help_text="Entrez la date de retour prévue de l'exemplaire")
    numero_exemplaire = models.CharField(max_length=20, help_text="Entrez le numéro de l'exemplaire")
    LOAN_STATUS = (
        ('m', 'Maintenance'),
        ('e', 'Emprunté'),
        ('d', 'Disponible'),
        ('r', 'Réservé'),
    )
    status= models.CharField(
        max_length=1,
        choices=LOAN_STATUS,
        blank=True,
        default='m',
        help_text='disponibilité Livre',
    )
    
    class Meta:
        ordering = ['date_retour']

    def __str__(self):
        return f" {self.numero_exemplaire} ({self.livre.titre}) - {self.get_status_display()})"
    
   # def get_absolute_url(self):
    #    return reverse('detail_exemplaire', args=[str(self.id)] )
    
class Auteur(models.Model):
    prenoms = models.CharField(max_length=100, help_text="Entrez le prénom de l'auteur")
    nom = models.CharField(max_length=100, help_text="Entrez le nom de l'auteur")
    date_naissance = models.DateField(null=True, blank=True, help_text="Entrez la date de naissance de l'auteur")
    date_de_deces = models.DateField('Décédé', null=True, blank=True, help_text="Entrez la date de décès de l'auteur")
    
    class Meta:
        ordering = ['nom', 'prenoms']

    def get_absolute_url(self):
        return reverse('detail_auteur', args=[str(self.id)])
    
    def __str__(self):
        return f"{self.prenoms} {self.nom}"
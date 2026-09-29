import uuid
from django.db import models
from django.urls import reverse


class Etudiant(models.Model):
    TITRE_CHOICES = (
        ('M', 'Monsieur'),
        ('Mme', 'Madame'),
        ('Mlle', 'Mademoiselle'),
    )
    
    nom = models.CharField(max_length=40, null=True, blank=True, help_text="Entrez le nom de l'étudiant")
    prenom = models.CharField(max_length=100, null=True, blank=True, help_text="Entrez le prénom de l'étudiant")
    email = models.EmailField(unique=True, null=True, blank=True, help_text="Entrez l'email de l'étudiant")
    titre = models.CharField(max_length=10, choices=TITRE_CHOICES, help_text="Sélectionnez le titre de l'étudiant")

    class Meta:
        ordering = ['nom', 'prenom']

    def __str__(self):
        return f"{self.prenom} {self.nom}"


class Genre(models.Model):
    nom = models.CharField(max_length=200, help_text="Entrez le nom du genre (ex: Littérature, Science-fiction, etc.)")

    def __str__(self):
        return self.nom


class Auteur(models.Model):
    prenoms = models.CharField(max_length=100, help_text="Entrez le prénom de l'auteur")
    nom = models.CharField(max_length=100, help_text="Entrez le nom de l'auteur")
    date_naissance = models.DateField(null=True, blank=True, help_text="Date de naissance")
    date_de_deces = models.DateField('Décédé', null=True, blank=True, help_text="Date de décès")
    
    class Meta:
        ordering = ['nom', 'prenoms']

    def get_absolute_url(self):
        return reverse('detail_auteur', args=[str(self.id)])
    
    def __str__(self):
        return f"{self.prenoms} {self.nom}"


class Livre(models.Model):
    titre = models.CharField(max_length=200, help_text="Entrez le titre du livre")
    auteur = models.ForeignKey(Auteur, on_delete=models.SET_NULL, null=True, help_text="Auteur du livre")
    resume = models.TextField(max_length=1000, help_text="Résumé du livre")
    isbn = models.CharField('ISBN', max_length=13, unique=True, help_text="Code ISBN (13 caractères)")
    genre = models.ManyToManyField(Genre, help_text="Sélectionnez le ou les genres du livre")
    
    def __str__(self):
        return self.titre

    def get_absolute_url(self):
        return reverse('detail_livre', args=[str(self.id)])


class Exemplaire(models.Model):
    LOAN_STATUS = (
        ('m', 'Maintenance'),
        ('e', 'Emprunté'),
        ('d', 'Disponible'),
        ('r', 'Réservé'),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text="Identifiant unique de l'exemplaire")
    livre = models.ForeignKey(Livre, on_delete=models.SET_NULL, null=True, help_text="Livre correspondant")
    numero_exemplaire = models.CharField(max_length=20, help_text="Numéro d'inventaire / Code-barres")
    date_retour = models.DateField(null=True, blank=True, help_text="Date de retour prévue")
    status = models.CharField(
        max_length=1,
        choices=LOAN_STATUS,
        blank=True,
        default='m',
        help_text='Disponibilité du livre',
    )
    emprunteur = models.ForeignKey(
        Etudiant, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        help_text="Étudiant ayant emprunté cet exemplaire"
    )

    class Meta:
        ordering = ['date_retour']

    def __str__(self):
        return f"{self.numero_exemplaire} ({self.livre.titre if self.livre else 'Sans titre'}) - {self.get_status_display()}"
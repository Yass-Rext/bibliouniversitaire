# BiblioUniv — Gestion de bibliothèque universitaire

Application Django de gestion de catalogue et de prêts pour une bibliothèque universitaire.
Elle permet de référencer les ouvrages (livres, auteurs, genres), de suivre les exemplaires
physiques et les étudiants emprunteurs, le tout depuis une interface web avec un panneau
d'administration complet.

## Fonctionnalités

### Catalogue public

- **Tableau de bord** (`/`) : statistiques du catalogue (nombre de livres, d'exemplaires,
  d'auteurs, d'étudiants), taux de disponibilité et liste des 5 dernières acquisitions.
- **Recherche** : recherche par titre, nom ou prénom d'auteur, ou ISBN, depuis la page
  d'accueil ou la page catalogue. La recherche est insensible à la casse.
- **Liste paginée** : 10 livres par page, avec affichage des genres en badges.
- **Fiche détaillée** : résumé, ISBN, genres, disponibilité globale et tableau des exemplaires
  (numéro d'inventaire, statut, date de retour, emprunteur).
- **Ajout de livre** : formulaire de création validé côté serveur, avec redirection vers la
  fiche du livre créé.

### Administration Django (`/admin/`)

- **Etudiant** : colonnes nom / prénom / titre / email, recherche et filtre par titre.
- **Auteur** : regroupement des dates de naissance et de décès sur une même ligne.
- **Livre** : double liste de sélection des genres (`filter_horizontal`) et gestion
  intégrée des exemplaires via un inline.
- **Exemplaire** : recherche par numéro d'exemplaire, livre ou emprunteur ; regroupement
  des champs en sections ; identifiant UUID en lecture seule.
- **Exemplaire** : statut par défaut `Maintenance` à la création, modifiable en inline
  depuis la fiche d'un livre.

## Stack technique

| Élément | Valeur |
| --- | --- |
| Framework | Django 6.1 |
| Langage | Python 3.12 |
| Base de données | SQLite 3 (`db.sqlite3`) |
| Frontend | Templates Django + Bootstrap 5 (CDN) |
| Gestion de dépendances | uv (`pyproject.toml` + `uv.lock`) |

## Prérequis

- Python 3.12 ou supérieur
- [uv](https://docs.astral.sh/uv/) (optionnel, mais recommandé)

## Installation

```bash
# 1. Installer les dépendances
uv sync
# ou, avec pip :
uv export --format requirements-txt | pip install -r -

# 2. Appliquer les migrations
python manage.py migrate

# 3. Créer un compte administrateur
python manage.py createsuperuser

# 4. Démarrer le serveur de développement
python manage.py runserver
```

L'application est accessible sur <http://127.0.0.1:8000/> et l'administration sur
<http://127.0.0.1:8000/admin/>.

### Séquence de mise en route des données

L'ordre compte, car les modèles sont liés entre eux par des clés étrangères :

1. **Genre** — créer les catégories (Littérature, Science-fiction, …)
2. **Auteur** — renseigner les auteurs
3. **Livre** — rattacher chaque livre à un auteur, un ISBN et un ou plusieurs genres
4. **Etudiant** — inscrire les étudiants
5. **Exemplaire** — rattacher les exemplaires à un livre, passer le statut à `Disponible`
   et renseigner l'emprunteur pour les prêts

## Structure du projet

```
.
├── apps/
│   └── catalogue/              # Application métier unique
│       ├── admin.py            # Configuration de l'administration
│       ├── apps.py             # CatalogueConfig
│       ├── forms.py            # LivreForm, AuteurForm, EtudiantForm, EmpruntForm
│       ├── models.py           # Genre, Auteur, Livre, Exemplaire, Etudiant
│       ├── urls.py             # Routes de l'application
│       ├── views.py            # index, liste_livres, detail_livre, ajouter_livre
│       ├── tests.py
│       └── migrations/
├── bibliouniversitaire/        # Configuration du projet
│   ├── settings.py             # INSTALLED_APPS, templates, base de données
│   ├── urls.py                 # URLs racine
│   ├── asgi.py
│   └── wsgi.py
├── templates/                  # Templates du projet (DIRS dans settings.py)
│   ├── base.html               # Structure commune : navbar, footer
│   ├── index.html              # Tableau de bord
│   └── catalogue/
│       ├── livre_list.html     # Catalogue avec recherche et pagination
│       ├── livre_detail.html   # Fiche d'un livre
│       ├── livre_form.html     # Formulaire d'ajout
│       └── indexbackup.html    # Ancien template conservé pour référence
├── static/                     # css / js / images
├── db.sqlite3
├── manage.py
├── pyproject.toml
└── uv.lock
```

### Modèle de données

| Modèle | Champs principaux | Relations |
| --- | --- | --- |
| `Genre` | `nom` | — |
| `Auteur` | `prenoms`, `nom`, `date_naissance`, `date_de_deces` | — |
| `Livre` | `titre`, `resume`, `isbn` (unique, 13 car.) | FK `auteur`, M2M `genre` |
| `Etudiant` | `titre`, `nom`, `prenom`, `email` (unique) | — |
| `Exemplaire` | `id` (UUID), `numero_exemplaire`, `status`, `date_retour` | FK `livre`, FK `emprunteur` |

Statuts d'un `Exemplaire` : `m` Maintenance (défaut), `d` Disponible, `e` Emprunté,
`r` Réservé.

Les relations `livre` et `emprunteur` sont nullables : supprimer un livre ou un étudiant
ne supprime pas les exemplaires mais les détache (`SET_NULL`).

## Routes

| URL | Nom | Description |
| --- | --- | --- |
| `/` | `pageacceuil` | Tableau de bord |
| `/catalogue/` | `index` | Dashboard (vue catalogue) |
| `/catalogue/livres/` | `liste_livres` | Catalogue avec recherche et pagination |
| `/catalogue/livre/ajouter/` | `ajouter_livre` | Formulaire d'ajout d'un livre |
| `/catalogue/livre/<pk>/` | `detail_livre` | Fiche détaillée d'un livre |
| `/admin/` | — | Administration Django |
| `/hello/` | — | Page d'erreur 500 (route de test) |

## Commandes utiles

```bash
python manage.py check              # Vérifier la configuration
python manage.py makemigrations      # Générer les migrations
python manage.py migrate             # Appliquer les migrations
python manage.py test                # Lancer les tests
python manage.py createsuperuser     # Créer un compte admin
python manage.py shell               # Console Python avec l'environnement Django
python manage.py runserver           # Serveur de développement
```

## Limites connues

- Le lien « Gérer les prêts » du tableau de bord pointe vers
  `/admin/circulation/exemplaire/`. L'application s'appelle `catalogue` : le bon chemin
  est `/admin/catalogue/exemplaire/`.
- `Auteur.get_absolute_url()` référence la route `detail_auteur`, qui n'est pas encore
  définie dans `apps/catalogue/urls.py`.
- `AuteurForm`, `EtudiantForm` et `EmpruntForm` sont définis mais pas encore utilisés par
  une vue ; seuls `LivreForm` et l'administration sont actifs.
- `SECRET_KEY` et `DEBUG = True` sont des valeurs de développement. À remplacer par des
  variables d'environnement avant toute mise en production.
- `apps/catalogue/tests.py` est vide : aucun test automatisé ne couvre encore l'application.
- Aucun suivi des prêts (historique, retards, pénalités) n'est encore implémenté.

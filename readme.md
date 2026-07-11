# Logiciel de gestion de tournois d'echecs

## Installation:

- Installer Python 3.12 ou supérieur.
- Configurer un environnement virtuel avec venv.
- Initialiser l'environnement virtuel, puis se placer dans le dossier du projet.
- Avec pip installer les dépendances requises par le projet en utilisant le fichier requirements.txt
- Depuis le terminal, avec l'environnement virtuel activée, lancer l'application avec la commande "py main.py"

## Utilisation du logiciel:

- Le logiciel fonctionne directement dans le terminal.
- Les actions disponibles sont affichées, préfixées d'un numéro. Pour effectuer une action il suffit de taper le numéro et de valider avec "Entrée"
- Saisies des données demandée: Un format spécifique est attendu pour chaque entrée. La saisie sera à recommencer tant que le format est invalide.
- Une action commencée doit être terminée. (Amélioraton : L'annulation de l'action en cours est éventuellement une fonctionnalité à implémenter dans une future mise à jour)

## Gérer les joueurs de la base de données:
- Sélectionner "Handle Players" dans le menu principal

### Créer un joueur:
- Sélectionner "Create new player"
- Renseigner les informations demandées.
- Le chess ID doit être unique. Le joueur est rejeté si le chess id existe déjà. (Amélioraton : Rejet dès la saisie du chess id).

### Voir tous les joueurs:
- Sélectionner "Show Players". L'intégralité des joueurs est affichée, classée par ordre alphabétique (Nom de famille)

## Gérer les tournois:
- Sélectionner "Handle Tournaments" dans le menu principal

### Créer un nouveau tournoi:
- Sélectionner "Create new tournament"
- Renseigner les informations demandées.

### Afficher tous les tournois:
- Sélectionner "Show all tournaments". L'intégralité des tournois est affichée.

### Gérer le déroulement d'un tournois:
- Sélectionner "Handle tournament"
- Renseigner partiellement (quelques lettres suffisent) le nom du tournois. Les tournois au nom le plus proche seront alors affichés, et sélectionnables comme les menus. Si un seul tournois correspond au nom tapé, il est automatiquement sélectionné.
    - "Show tournament details" permet de revoir les informations du tournois
    - "Register players" permet d'inscrire un joueur au tournoi. Fonctionne comme la sélection du tournoi, avec un nom complet ou partiel. Si un seul joueur correspond à la saisie, alors il est ajouté automatiquement. Les joueurs ne peuvent pas être ajouté en double.
    - "Show registered players" permet de voir les jouers inscrits
    - "Run tournament" permet de -jouer- le tournois. Voir section suivante.
    - "Show standings" permet de voir le classement du tournoi
    - "Show tournament rounds" permet de voir les résultat, de chaque ronde, pour chaque match.

### Jouer un tournoi:
- Le tournoi est -joué-:
    - La première ronde est générée aléatoirement avec tous les joueurs inscrits.
    - Pour chaque match, il faut sélectionner le vainqueur, ou match nul.
    - Lorsque tous les matchs sont renseignés, il est possible de continuer ou d'arrêter de -jouer-.
    - lorsque toutes les rondes sont complètes, le tournoi est terminé.
    

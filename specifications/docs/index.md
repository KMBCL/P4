# P4

Logiciel hors ligne.

Ecrit en python

Executé en lignes de commandes

Stockage des données au format JSON

Entités définies:

- Joueur
- Tournois:
    -   A un nombre de tours:
        - Un tour est une liste de Match:
            - Un match est une paire de joueurs
            - Score:
                - Un gagant >> 1 point pour le gagnant
                - Nul >> 0.5 points pour les duex joueurs
                - Perdant >> 0 point




Tour : liste de matches
Match : tuple de liste -> match = tuple[list[player, score], list[player, score]]
list[player, score] -> peut être un objet Match?


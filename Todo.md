### Trouver un moyen d'héberger ça en local, le script se lance une seule fois a 10h et a 17h30

avoir une condition dans spot.json : excludeDay + fromDate-toDate pour comté pas dimanche en chasse, bondue pas semaine hors été, sangatte pas été...

Faire fonctionner depuis mon ordi perso en double run avec cron décallé l'un de l'autre
Orienter objet pour plus de clarté

Pas besoin de clone a chaque fois, juste un pull des branches

Avoir un systeme de tagging, une staging=branche depuis config.json, preprod=main, prod=tag depuis config.json

Quand on publie une nouvelle release, envoyer un message Signal avec les nouveautés a comprendre

Mettre les horaire de marée pour les spots de bord de mer, 1h30 avant/après marée haute
Mettre lien meteo-blue + lien Balise

Est-ce qu'un modele de Windy est meilleurs qu'un autre a moyen-terme, long-terme, court-terme ?
Pour faire ça besoin de persistence et comparaison avec balise

Librairie pour créer une image texte et avoir de la mise en forme du coup
https://python.plainenglish.io/generating-text-on-image-with-python-eefe4430fe77

# WindyParser
remettre les bonnes logs

Faire une github pages avec sender class qui commit markdown 
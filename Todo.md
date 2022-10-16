### Dev
Mettre lien windy + model Arome + lien Balise en entete de spot

Mettre en header de site + signal : model Arome de Windy, mis a jour a la date de

mettre localisation en description de spot

cron tous les 30 mn -> check date mise a jour Arome, si update faire le process

Mettre les horaire de marée pour les spots de bord de mer, 1h30 avant/après marée haute

Mettre prévision meteo-france pour la pluie heure par heure si possible
Mettre risque orage 

s'abonner a windy premium pour un mois et voir si je peux avoir les previsions heure par heure avec selenium

Pour les spots de la date du jour, mettre résultat balise depuis ce matin + prévision de toute la journée avec bon créneau en vert. Il faut pouvoir comparer windy et la balise d'un coup d'oeil dans un tableau

Faire page site récapitulative des spots et des conditions

mettre tous les modeles windy si un des models est bon : si GFS ok prend tout, si Arome ok prend tout. Et mettre ça sous forme de tableau

Screenshot par site pour windy, meteo-parapente, meteoblue que je met dans une page lié en href au nom du spot

### Prod
hebergement OVH

Ansible sur VM OVH :
- un playbook pour l'installation
- un playbook lié a un cron pour le run

Bug locale 2h de moins sur serveur OVH

Pas besoin de clone a chaque fois, juste un pull des branches
Avoir un systeme de tagging, une staging=branche depuis config.json, preprod=main, prod=tag depuis config.json

monit qui check si tout tourne bien

mettre du google analytics pour savoir popularité

Faire de la doc de mise en prod pour le repo : dev en local, description option, idée d'exploit : ansible + cron, local + stdout





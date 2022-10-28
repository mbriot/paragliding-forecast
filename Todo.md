### Dev

Sur page allDays : trier par score de "possibilité de vol" : avoir par jour le spot le moins pourri
> Si le système de score est bien fait, les endroits ou on vol une fois en vert remonte en premier
puis bonne direction plus de point que pas de pluie, vent trop fort plus de point que pas beaucoup de pluie
Peut etre ne pas prendre en compte la pluie ?
Ou tout simplement distance vent en degré la plus proche?

Faire en sorte que Date = deroulable/fermable

Faire une page par spot en lié par lien href avec les 2 pages principales

Ajouter les horaire de marée pour les spots de bord de mer, 1h30 avant/après marée haute


Faire une passe de black, pylint  flake8 sur le code. Faire tourner ça avec Tox ?

Mettre prévision meteo-france pour la pluie heure par heure si possible
Mettre risque orage 

Logfile appender dans /var/log/paragliding-forecast

s'abonner a windy premium pour un mois et voir si je peux avoir les previsions heure par heure avec selenium

Pour les spots de la date du jour, mettre résultat balise depuis ce matin + prévision de toute la journée avec bon créneau en vert. Il faut pouvoir comparer windy et la balise d'un coup d'oeil dans un tableau

mettre tous les modeles windy si un des models est bon : si GFS ok prend tout, si Arome ok prend tout. Et mettre ça sous forme de tableau

Screenshot par site pour windy, meteo-parapente, meteoblue que je met dans une page lié en href au nom du spot

### Prod

Customiser la 404 avec un truc marrant

logrotation daily keep 5 dans /var/log/paragliding-forecast

exposer service http : https://docs.ovh.com/fr/dedicated/firewall-iptables/

preprod = preprod.markdown qui prend spot_test.json et config_test.json en paramètre, voir ansible pour avoir config de preprod et de prod
preprod joué 2 fois par jour et envoi signal + web tous le temps

config prod = tag=xxx, spot_file= spots.json, config_file=config.json
config preprod = branch=main, spot_file= spot_test.json, config_file=config_test.json

monit qui check si tout tourne bien

Faire de la doc de mise en prod pour le repo : dev en local, description option, idée d'exploit : ansible + cron, local + stdout

send mail avec gmail : https://www.howtoforge.com/tutorial/configure-postfix-to-use-gmail-as-a-mail-relay/

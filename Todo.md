### Dev

Bug : pour les precipitations, des fois il se peut que j'ai 0.3cm au lieu de 0.3mm et ça ppète la regex

Renommer --send-to-website en --generate-markdown

Faire une page par jour

Faire un lien par spot vers son id dans about pour avoir rapidement description

Ajouter les horaire de marée pour les spots de bord de mer, 1h30 avant/après marée haute

Faire un second site pour avoir normandie et autre pour les gros weekends
- création repo
- ajout mbriot repo
- cron dédié pour les spots
- fichier de spots.json a créer
- qu'a partir du mercredi jusqu'au vendredi midi
- avoir une page par fichier de spot : normandie.json, sedan.json, troyes.json, reims.json...

Ajouter des tests unitaires avec pytest

Faire une passe de black, pylint  flake8 sur le code. Faire tourner ça avec Tox ?

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

["O","OSO","SSO","SO","SE","N","NE","NNE","NNO","ESE","E","S", "SSE", "SE"]

python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt 

Add geckodriver binary somewhere + export PATH=$PATH:/path/to/gecko

python main.py --spot-file=./spots_test.json --config-file=./config_test.json -v --send-to-signal
- spot-file : listes des spots en json
- config-file : signal credentials
- -v : log au format debug
- send-to-signal : send the result in Signal app, will not do it if not present

### Send result via Signal App

`docker run -d --name signal-api --restart=always -p 8080:8080       -v $HOME/.local/share/signal-cli:/home/.local/share/signal-cli       -e 'MODE=native' bbernhard/signal-cli-rest-api:0.112-dev`

WARNING : backuper $HOME/.local/share/signal-cli en passage en prod
Si pas de backup : generer QrCode et le scanner avec Signal : http://localhost:8080/v1/qrcodelink?device_name=signal-api 
Mais du coup accés que aux groupes créés par cette instance

And then follow documentation to register : 
Doc : https://github.com/bbernhard/signal-cli-rest-api
Swagger : https://bbernhard.github.io/signal-cli-rest-api/#/Groups/get_v1_groups__number_

// Group Id : seulement ceux que j'ai créé via l'API
curl -X GET -H "Content-Type: application/json" 'http://localhost:8080/v1/groups/+33XXXXX' 

// Send to someone specificaly
curl -X POST -H "Content-Type: application/json" 'http://localhost:8080/v2/send' \
     -d '{"message": "Test via Signal API!", "number": "+33XXXXX", "recipients": [ "+33XXXXX" ]}' 

// Create Group
curl -X 'POST' \
  'http://localhost:8080/v1/groups/%2B33XXXXX' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "description": "string",
  "group_link": "disabled",
  "members": [
    "+33607968615","+336XXXXX"
  ],
  "name": "Test Parapente",
  "permissions": {
    "add_members": "only-admins",
    "edit_group": "only-admins"
  }
}'

// Send message to group, need to create it before
curl -X POST -H "Content-Type: application/json" -d '{"message": "HELLO FROM AUTOMATED JAMES" , "number": "+3360XXXXX", "recipients": ["group.id"]}' 'http://localhost:8080/v2/send'

// Add members to group
curl -X 'POST' \
  'http://localhost:8080/v1/groups/+33XXXX/{groupid}/members' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "members": [
    "+336XXX",
    "+336XXXX"
  ]
}'


python3 src/main.py --config-file=/home/centos/config.json --spot-file=ardennes.json --send-to-new-regions --html-file=ardennes.markdown -v

python3 src/main.py --config-file=/home/centos/config.json --spot-file=spots.json --html-file=titi.markdown --send-to-website

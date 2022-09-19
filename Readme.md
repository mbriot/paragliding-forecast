python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt 

python main.py


Doc : https://github.com/bbernhard/signal-cli-rest-api
Swagger : https://bbernhard.github.io/signal-cli-rest-api/#/Groups/get_v1_groups__number_

// Group Id : seulement ceux que j'ai créé via l'API
curl -X GET -H "Content-Type: application/json" 'http://localhost:8080/v2/groups/%2B33XXXXX' 

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
#! /bin/bash
function log() { echo -e "\033[0;31m [$(date '+%F %T')] $1\033[0m";};
cd $1
git co automatization
git pull origin automatization

lastRun=`head -n1 status.txt | cut -d, -f2`
lastRunDay=$(date -jf "%d/%m/%YT%H:%M" $lastRun '+%s')
today=`date -jf "%d/%m/%YT%H:%M" $(date +%d/%m/%YT08:00) '+%s'`
log "lastRunDay = $lastRunDay"
log "today = $today"

if [ $lastRunDay -lt $today ]; then
  log "start checking weather"
  git co main
  git pull origin main
  source .venv/bin/activate
  pip3 install -r requirements.txt
  python3 main.py
  git co automatization
  git pull origin automatization
  echo "OK,$(date +%d/%m/%YT%H:%M)" > status.txt
  git commit -am "update status"
  git push origin automatization
else
  log "No need to process, already done"
fi
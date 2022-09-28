#! /bin/bash
function log() { echo -e "[shell-script][$(date '+%F %T')] $1";};
[[ $(/usr/sbin/lsof -t $0| wc -l) -gt 1 ]] && log "At least one of $0 is running, exit now"
[[ $(/usr/sbin/lsof -t $0| wc -l) -gt 1 ]] && exit 1
log "Starting script"
cd $1
checkWeatherAnyway=$2

log "Cloning repository"
git clone git@github.com:mbriot/paragliding-forecast.git
cd paragliding-forecast
git co automatization

log "Check if docker is running"
checkDocker=$(/usr/local/bin/docker ps | grep signal-api)
if [ "x" == "x${checkDocker}" ];then
 log "Error, Docker is not working";
 git co main;
 exit 1;
else
 log "Docker is working, let's continue";
fi

lastRun=`head -n1 status.txt | cut -d, -f2`
lastRunDay=$(date -jf "%d/%m/%YT%H:%M" $lastRun '+%s')
now=`date -jf "%d/%m/%YT%H:%M" $(date +%d/%m/%YT%H:%M) '+%s'`
eightAmHourToday=`date -jf "%d/%m/%YT%H:%M" $(date +%d/%m/%YT08:00) '+%s'`
sixPmHourToday=`date -jf "%d/%m/%YT%H:%M" $(date +%d/%m/%YT18:00) '+%s'`

if [[ $now -gt $eightAmHourToday && $lastRunDay -lt $eightAmHourToday ]] || [[ $now -gt $sixPmHourToday && $lastRunDay -lt $sixPmHourToday ]]; then
  log "start checking weather"
  git co main
  source .venv/bin/activate
  pip3 install -r requirements.txt
  python3 main.py --spot-file=../spots.json --config-file=../config.json --send-to-signal -v
  git co automatization
  echo "OK,$(date +%d/%m/%YT%H:%M)" > status.txt
  git commit -am "update status"
  git push origin automatization
else
  log "No need to process, already done"
fi

cd ..
rm -rf paragliding-forecast

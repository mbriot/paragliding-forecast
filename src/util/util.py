from datetime import datetime 

def getResultByDay(weekPrediction):
    resultByDay = {}
    for spotResult in weekPrediction:
        spotName = spotResult["name"]
        for date in spotResult["dates"]:
            if resultByDay.get(date["day"],None) is None:
                resultByDay[date["day"]] = {}
            for slot in date["slots"]:
                slot["name"] = spotName
                if resultByDay[date["day"]].get(spotName,None) is None:
                    resultByDay[date["day"]][spotName] = []
                resultByDay[date["day"]][spotName].append(slot)
    
    return resultByDay

def sortByDate(weekPrediction):
    sortedPrediction = {}
    for date in sorted(weekPrediction.keys()):
        sortedPrediction[datetime.fromtimestamp(int(date)).strftime('%A %d %B')] = weekPrediction[date]
    return sortedPrediction


def getDaysWithAtLeastOneSlot(weekPrediction):
    flyablesDay = {}
    for date in weekPrediction:
        for spot, hours in weekPrediction[date].items():
            flyableHours = list(filter(lambda x: x.get('flyable') == True, hours))
            if len(flyableHours) == 0:
                continue
            if flyablesDay.get(date,None) is None and len(flyableHours) > 0:
                flyablesDay[date] = {}
            if flyablesDay.get(date,None) is not None and flyablesDay[date].get(spot,None) is None and len(flyableHours) > 0:
                flyablesDay[date][spot] = []
            if len(flyableHours) > 0:
                flyablesDay[date][spot] = flyablesDay[date][spot] + hours
    return flyablesDay

def getDaysWithOnlyFlyablesSlots(weekPrediction):
    flyablesDay = {}
    for date in weekPrediction:
     for spot, hours in weekPrediction[date].items():
        flyableHours = list(filter(lambda x: x.get('flyable') == True, hours))
        if flyablesDay.get(date,None) is None and len(flyableHours) > 0:
            flyablesDay[date] = {}
        if flyablesDay.get(date,None) is not None and flyablesDay[date].get(spot,None) is None and len(flyableHours) > 0:
            flyablesDay[date][spot] = []
        if len(flyableHours) > 0:
            flyablesDay[date][spot] = flyablesDay[date][spot] + flyableHours
    return flyablesDay
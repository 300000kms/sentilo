# -*- coding: utf-8 -*-
'''

'''
import requests
import csv
import time

def save2csv(fileName, listoflists):
    with open(fileName, 'a+') as csvfile:
        csvwriter = csv.writer(csvfile)
        for l in listoflists:
            csvwriter.writerow(l)
    return


def getSensorsList():
    '''
    this function returns a list of the sensors available in the area defined in the url
    probably interesting improve the code introducing the area as an input variable
    '''
    url = 'http://connecta.bcn.cat/connecta-catalog-web/component/map/json?ts=1488883790884&bounds=41.037124%2C1.176559%2C41.744135%2C3.080971'
    r = requests.get(url)

    if r.status_code == 200:
        result = r.json()
        sensors = result['components']
        sensorList=[]
        for s in sensors:
            print s['id'], s['type'], s['centroid']['latitude'], s['centroid']['longitude']
            sensorList.append( [ s['id'], s['type'], s['centroid']['latitude'], s['centroid']['longitude'] ])
        return sensorList

    else:
        print  r.status_code
        return


def getDataSensor(sensor, debug):
    '''
    sensor: the id of the sensors
    '''
    timestamp =int(time.time()*1000)
    print [timestamp]
    url = 'http://connecta.bcn.cat/connecta-catalog-web/component/map/%s/lastOb/?ts=%s' %(sensor, timestamp)
    r = requests.get(url)
    if r.status_code==200:
        s = r.json()
        if debug is True:
            print s
        data = [s['sensorLastObservations'][0]['sensor'], s['sensorLastObservations'][0]['sensorState'], s['sensorLastObservations'][0]['value']]
        save2csv('sensorsData.csv', [data])
    else:
        return None

    return


def getDataLoop(listofsensors, debug):
    while True:
        for s in listofsensors:
            getDataSensor(s, debug)
        time.sleep(60)
    return



if __name__ == "__main__":
    ## get the list of available sensors and put on a csv
    #save2csv('sensors.csv', getSensorsList())
    listofsensors=['CESVA.TA120-T240712', 'CESVA.TA120-T240996', 'CESVA.TA120-T240424','CESVA.TA120-T241196', 'CESVA.TA120-T241000']
    getDataLoop(listofsensors,True)

import redis
import json
import base64


# Holds a list of all the durations of each phase, used for average numbers later
phases = {'router': [], 'balancer': [], 'plugin': [], 'access.before': [], 'access.after': [], 'connect.toip': [], 'query': [], 'cassandra_iterate': [], 'balancer.getPeer': [], 'load_plugin_config': [] }

def avg(phase):
    
    xt = 0
    for i in phase:
        xt += i
    try:
        axt = round((xt / len(phase) / 1000), 2)
    except ZeroDivisionError:
        axt = xt
    return axt

store = redis.StrictRedis("0.0.0.0", '6379', charset="utf-8", decode_responses=True)

fileName = '/home/teknetik/Downloads/tracing/172.21.106.162-tracing.log'

def storeData():
    store.flushall()
    traceNum = 0
    with open (fileName, "r") as file:
        print("Reading File")
        for i in file:
            trace = json.loads(i)
            #print(trace)
            for k,v in trace[0].items():
                if isinstance(v, dict):
                    for k1,v1 in v.items():
                        store.hset(str(traceNum), str(k)+"."+str(k1), str(base64.b64decode(v1).decode('UTF-8')))
                else:
                    store.hset(str(traceNum), str(k), str(v))
                
                for n in phases:
                    if trace[0]['name'] in n:
                        phases[n].append(trace[0]['duration'])
                    else:
                        pass
            
            for i in phases:
                if len(phases[i]) > 0:
                    store.hset("PhaseAvg", i, avg(phases[i]))

            #print(phases)            
            #print(traceNum)    
            traceNum +=1




# Return to x most expensive traces. int=number of results
def topCost(num):
    costData={}
    for key in store.scan_iter("[0-9]*"):
        duration = store.hget(key,"duration")
        costData[key]=duration
        rankedResult=sorted(costData.items(), key=lambda item: item[1], reverse=False)
    topData = {}
    for key in rankedResult[0:num]:
        key=key[0]
        duration = store.hget(key,"duration")
        name = store.hget(key,"name")
        topData[key]={}
        topData[key]['duration']=duration
        topData[key]['name']=name
    return topData




def getTraceData(traceId):
    traceData = store.hgetall(traceId)
    return traceData

# Nested keys are stored in redis as 'data.plugin' for example, this function returns it back to a nested dict
def transform(traceData):
    try:
        for i in traceData:
            if "data." in i:
                if traceData.get('data') is None:
                    traceData['data']={}
                a = str(i).split(".")
                traceData['data'][a[1]]=traceData['data.'+a[1]]
                key = str(a[0]) + "." + str(a[1])
                del traceData[key]
    except RuntimeError:
        transform(traceData)
    return traceData


def getPhaseAvg():
    PhaseAvg = store.hgetall('PhaseAvg')
    return PhaseAvg


#storeData()
# traceData = getTraceData(104)
# print(transform(traceData))
#getPhaseAvg()
#topCost(10)
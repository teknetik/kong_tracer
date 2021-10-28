import json
from collections import OrderedDict
from operator import itemgetter    
import sys
import base64

fileName=sys.argv[1]
try:
    debug=sys.argv[2]
except IndexError:
    debug=False


if debug == 'debug':
    debug=True


# threshold in seconds [ 1000000 = 1(s) ]
# https://docs.konghq.com/enterprise/2.3.x/property-reference/#tracing_time_threshold



# Holds a list of all the durations of each phase, used for average numbers later
phases = {'router': [], 'balancer': [], 'plugin': [], 'access.before': [], 'access.after': [], 'connect.toip': [], 'query': [], 'cassandra_iterate': [], 'balancer.getPeer': [], 'load_plugin_config': [] }

# Hold the raw JSON trace data as a python obj
rawData = {}
# Contains custom data for parsing
data = {}
# Number of traces processed
traceNum = 0
# Number of traces over the threshold duration limit
traceThresCount = 0
threshold = 5000
results = {}

def avg(phase):
    
    xt = 0
    for i in phase:
        xt += i
    try:
        axt = round((xt / len(phase) / 1000), 2)
    except ZeroDivisionError:
        axt = xt
    return axt

#with open ("/home/teknetik/Downloads/trace_json/tracing_small.json", "r") as file:
with open (fileName, "r") as file:
    print("Reading File")
    for i in file:
        trace = json.loads(i)
        rawData[traceNum] = trace
        
        data[traceNum] = {}
        data[traceNum]['duration']= 0
        data[traceNum]['start']= []
        data[traceNum]['done']= []
        data[traceNum]['requestTime']= 0
        
        for e in trace:
            data[traceNum][e['id']]={'start': 0, 'done': 0, 'duration': 0}
            
            for n in phases:
                if e['name'] in n:
                    phases[n].append(e['duration'])
                else:
                    pass
            data[traceNum]['duration'] += e['duration']
            data[traceNum][e['id']]['duration'] = e['duration']
            
            data[traceNum]['start'].append(e['start'])
            data[traceNum]['done'].append(e['done'])
            data[traceNum][e['id']]['start']= e['start']
            data[traceNum][e['id']]['done']= e['done']
            
        traceNum +=1
    
    print("Generating Data")
    for i in data:
        
        timeSortStart = sorted(data[i]['start'])
        timeSortDone = sorted(data[i]['done'])

        firstStart = timeSortStart[0]
        lastDone = timeSortDone[-1]
        
        data[i]['requestTime'] = (lastDone - firstStart)

        
        if data[i]['duration'] > threshold:
            if debug:
                print("Request: " + str(i) + "  |  Request time: " + str(round(data[i]['requestTime'], 2)) + " s  |  Kong Processing Duration: " + str(data[i]['duration']) + " μs")
            
            results[i] = data[i]['duration']
        
        rankedResult=sorted(results.items(), key=lambda item: item[1], reverse=True)
            
        traceThresCount += 1

print("\n\nREQUESTS PROCESSED\n\n")

print("Number of traces processed: " + str(len(data)))
print("Number of requests taking longer than threshold value of " + str(threshold) + "s : " + str(traceThresCount))

print("\n\nAVERAGES ACROSS ALL SAMPLES\n\n")

for i in phases:
    if len(phases[i]) > 0:
        print(i + " phase: " + str(avg(phases[i])) + "ms")


finalResult=[]  
phases = {'router': [], 'balancer': [], 'plugin': [], 'access.before': [], 'access.after': [], 'connect.toip': [], 'query': [], 'cassandra_iterate': [], 'balancer.getPeer': [], 'load_plugin_config': [] }      
print("\n\nDisplaying data for top 10 expensive requests:\n")
for i in rankedResult[0:9]:
    print("Request: " + str(i[0]) + "  |  Kong Processing Duration: " + str(i[1]) + " μs")

print("\n\nDISPLAY TOP 10 DEBUG")
for i in rankedResult[0:9]:
    encodedData={}
    if debug:
        print(print("\nRequest: " + str(i[0]) + "  |  Request time: " + str(round(data[i[0]]['requestTime'], 2)) + " s  |  Kong Processing Duration: " + str(data[i[0]]['duration']) + " μs"))
        for requestData in rawData[i[0]]:
            for n in requestData['data']:
                
                encodedData[n] = base64.b64decode(requestData['data'][n])

        print(json.dumps(rawData[i[0]], indent=2))
        if encodedData:
            print("\n\nRequest: " + str(i[0]) + " ENCODED DATA\n")
            for k,v in encodedData.items():
                print(str(k) + ": " + str(v) + "\n")
    finalResult.append(rawData[i[0]])


#print(json.dumps(finalResult, indent=2))
for i in finalResult:
    for a in i:
        for n in phases:
            if a['name'] in n:
                phases[n].append(a['duration'])
            else:
                #print("failed on " + a['name'] + "matching " + str(phases[n]))
                pass
print("\nThe problem probably resides in the phase with the longest average duration below, this maybe one or more phases\n\n")   
for i in phases:
    if len(phases[i]) > 0:
        print(i + " phase: " + str(avg(phases[i])) + "ms")


if not debug:
    print("\n\n\nFor more detailed information run this script with debug:")
    print("    trace.py <file_name> debug")






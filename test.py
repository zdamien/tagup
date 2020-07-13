import requests
import json, sys

URL_base = "http://mindstalk.net:8000/api/"

print("Creating:")
payload = {'timestamp': 10000, 'value1': 'v1', 'value2': 1.2, 'value3': False}
r = requests.post(URL_base+'create', json = payload)
retval = r.json()
print(r.status_code, retval)
payload = {'timestamp': 20000, 'value1': 'v2', 'value2': 2.4, 'value3': True}
r = requests.post(URL_base+'create', json = payload)
retval = r.json()
print(r.status_code, retval)


print("Listing:")
r = requests.get(URL_base+'list')
print(r.status_code, r.json())

print("Getting first record:")
first = str(r.json()[0])
r = requests.get(URL_base+'read/'+first)
print(r.status_code, r.json())

print("Creating:")
payload = {'timestamp': 30000, 'value1': 'v3', 'value2': 3.6, 'value3': False}
r = requests.post(URL_base+'create', json = payload)
retval = r.json()
print(r.status_code, retval)

print("Bad create:")
payload = {'timestamp': 10000, 'value1': 'string too long', 'value2': 1.3, 'value3': False}
r = requests.post(URL_base+'create', json = payload)
print(r.status_code, r.reason)

print("Re-fetching:")
r = requests.get(URL_base+'read/'+ str(retval["id"]))
print(r.status_code, r.json())


r = requests.get(URL_base+'read/'+first)
d = r.json()
d['value2'] += 1
print("Modifying first record:")
r = requests.put(URL_base+'modify/'+first, json=d)
print(r.status_code, r.json())
print("Debugging first record:")
r = requests.get(URL_base+'debug/'+first)
print(r.status_code, r.json())

print("Bad modify:")
d['value1'] = "line far too long"
r = requests.put(URL_base+'modify/'+first, json=d)
print(r.status_code, r.reason)

print("Deleting first:")
r = requests.delete(URL_base+'remove/'+first)
print(r.status_code, r.text)
print("Listing:")
r = requests.get(URL_base+'list')
print(r.status_code, r.json())



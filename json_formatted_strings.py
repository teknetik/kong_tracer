import json
from json import decoder
import re
import base64

jsonstring="""[{
    "node_id": "d0444674-e194-47eb-9dc5-e66c3b91b331",
    "finished": true,
    "done": 1635324406.2653,
    "duration": 5484761,
    "date": "Wed, 27 Oct 2021 08:46:40 GMT",
    "id": "f47a2c61-8b6b-491b-a9e2-ba01e83ab0aa",
    "data": {
      "query": "U0VMRUNUICJpZCIsICJuYW1lIiwgRVhUUkFDVChFUE9DSCBGUk9NICJjcmVhdGVkX2F0IiBBVCBUSU1FIFpPTkUgJ1VUQycpIEFTICJjcmVhdGVkX2F0IiwgInJvdXRlX2lkIiwgInNlcnZpY2VfaWQiLCAiY29uc3VtZXJfaWQiLCAiY29uZmlnIiwgInByb3RvY29scyIsICJlbmFibGVkIiwgInRhZ3MiLCAid3NfaWQiCiAgRlJPTSAicGx1Z2lucyIKIFdIRVJFICJjYWNoZV9rZXkiID0gJ3BsdWdpbnM6cmF0ZS1saW1pdGluZy1hZHZhbmNlZDo1OTVhMTU3Ny1hNDg4LTQzNTMtODExOC1hMmU3ZWU0ZWEyMzY6OTZlMjNlYzctNTEwMi00MjE3LWEzN2QtNzNhZTllYTlmNjhlOmM4Y2VmMzI5LTBmM2QtNDkzZi04M2E4LWM5NjJhM2M5MzMxNDo6ZmZmMTBjMTQtZjkwNS00YWRiLWIyYzgtYWJlOGEzNzA1YjgzJwogICBBTkQgKCJ3c19pZCIgPSAnZmZmMTBjMTQtZjkwNS00YWRiLWIyYzgtYWJlOGEzNzA1YjgzJykKIExJTUlUIDE7",
      "traceback": "c3RhY2sgdHJhY2ViYWNrOgoJL3Vzci9sb2NhbC9zaGFyZS9sdWEvNS4xL2tvbmcvdHJhY2luZy9pbml0Lmx1YToxNzM6IGluIGZ1bmN0aW9uICdleGVjdXRlJwoJLi4ubG9jYWwvc2hhcmUvbHVhLzUuMS9rb25nL2RiL3N0cmF0ZWdpZXMvcG9zdGdyZXMvaW5pdC5sdWE6NjIxOiBpbiBmdW5jdGlvbiAnc2VsZWN0X2J5X2ZpZWxkJwoJL3Vzci9sb2NhbC9zaGFyZS9sdWEvNS4xL2tvbmcvZGIvZGFvL2luaXQubHVhOjEzMzg6IGluIGZ1bmN0aW9uICdzZWxlY3RfYnlfY2FjaGVfa2V5JwoJL3Vzci9sb2NhbC9zaGFyZS9sdWEvNS4xL2tvbmcvZGIvZGFvL3BsdWdpbnMubHVhOjM0NjogaW4gZnVuY3Rpb24gJ3NlbGVjdF9ieV9jYWNoZV9rZXknCgkvdXNyL2xvY2FsL3NoYXJlL2x1YS81LjEva29uZy9ydW5sb29wL3BsdWdpbnNfaXRlcmF0b3IubHVhOjc5OiBpbiBmdW5jdGlvbiA8L3Vzci9sb2NhbC9zaGFyZS9sdWEvNS4xL2tvbmcvcnVubG9vcC9wbHVnaW5zX2l0ZXJhdG9yLmx1YTo3OD4KCVtDXTogaW4gZnVuY3Rpb24gJ3hwY2FsbCcKCS91c3IvbG9jYWwvc2hhcmUvbHVhLzUuMS9yZXN0eS9tbGNhY2hlLmx1YTo3NDE6IGluIGZ1bmN0aW9uICdnZXQnCgkvdXNyL2xvY2FsL3NoYXJlL2x1YS81LjEva29uZy9jYWNoZS9pbml0Lmx1YToxNzg6IGluIGZ1bmN0aW9uICdnZXQnCgkvdXNyL2xvY2FsL3NoYXJlL2x1YS81LjEva29uZy9ydW5sb29wL3BsdWdpbnNfaXRlcmF0b3IubHVhOjExMTogaW4gZnVuY3Rpb24gJ2xvYWRfY29uZmlndXJhdGlvbicKCS91c3IvbG9jYWwvc2hhcmUvbHVhLzUuMS9rb25nL3J1bmxvb3AvcGx1Z2luc19pdGVyYXRvci5sdWE6MjEzOiBpbiBmdW5jdGlvbiAnbG9hZF9jb25maWd1cmF0aW9uX3Rocm91Z2hfY29tYm9zJwoJL3Vzci9sb2NhbC9zaGFyZS9sdWEvNS4xL2tvbmcvcnVubG9vcC9wbHVnaW5zX2l0ZXJhdG9yLmx1YTozMDY6IGluIGZ1bmN0aW9uICcoZm9yIGdlbmVyYXRvciknCgkvdXNyL2xvY2FsL3NoYXJlL2x1YS81LjEva29uZy9pbml0Lmx1YToyNzQ6IGluIGZ1bmN0aW9uICdleGVjdXRlX3BsdWdpbnNfaXRlcmF0b3InCgkvdXNyL2xvY2FsL3NoYXJlL2x1YS81LjEva29uZy9pbml0Lmx1YTo4OTE6IGluIGZ1bmN0aW9uICdhY2Nlc3MnCglhY2Nlc3NfYnlfbHVhKG5naW54LWtvbmcuY29uZjoxMDQpOjI6IGluIG1haW4gY2h1bms="
    },
    "start": 1635324400.7806,
    "name": "query",
    "parent": "c5a93875-1cc1-48d8-956b-5341bb8c8a06"
  },
  {
    "node_id": "d0444674-e194-47eb-9dc5-e66c3b91b331",
    "finished": true,
    "done": 1635324406.3014,
    "duration": 5521044,
    "date": "Wed, 27 Oct 2021 08:46:40 GMT",
    "id": "c5a93875-1cc1-48d8-956b-5341bb8c8a06",
    "data": {
      "plugin_name": "cmF0ZS1saW1pdGluZy1hZHZhbmNlZA=="
    },
    "start": 1635324400.7803,
    "name": "load_plugin_config"
  },
  {
    "node_id": "d0444674-e194-47eb-9dc5-e66c3b91b331",
    "finished": true,
    "done": 1635324409.4906,
    "duration": 3146681,
    "date": "Wed, 27 Oct 2021 08:46:46 GMT",
    "id": "d2bfb1f7-fc0f-4f64-b134-35043db589fe",
    "data": {},
    "start": 1635324406.344,
    "name": "access.after"
  }]"""

# This function can replace the decoded base64 from the trace data into a formatted string.

obj = json.loads(jsonstring)
string=json.dumps(obj, indent=2)
for field in obj[0]['data']:
  print(field)
  decoded = base64.b64decode(obj[0]['data'][field]).decode('UTF-8')
  print(decoded)
  print("\n\nregex")
  fieldSearch = r"\"" + field + "\":\s\"[aA-zZ,0-9,=]{1,999999}"
  fieldReplace = "\"" + field + "\":\"" + decoded + "\""
  print(re.sub(fieldSearch, fieldReplace, string))
  string = re.sub(fieldSearch, fieldReplace, string)
  print("\n\n")

print(string)

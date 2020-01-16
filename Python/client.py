import http.client

conn = http.client.HTTPConnection("127.0.0.1:8090")

payload = "{\n\t\"language\" : \"French\"\n}"

headers = { 'content-type': "application/json" }

conn.request("POST", "/postjson", payload, headers)

res = conn.getresponse()
data = res.read()

print(data.decode("utf-8"))

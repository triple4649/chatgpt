import requests, json

url = "http://localhost:11434/api/generate"
data = {
  "model": "gpt-oss:20b",
  "prompt": "hi:\n\n" + open("chatgpt.py").read()
}

with requests.post(url, json=data, stream=True) as r:
    for line in r.iter_lines():
        if line:
            j = json.loads(line)
            if "response" in j:
                print(j["response"], end="", flush=True)
            if j.get("done"):
                break
print()